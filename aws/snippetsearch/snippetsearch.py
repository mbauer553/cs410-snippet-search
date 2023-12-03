from opensearchpy import OpenSearch, helpers, RequestsHttpConnection
import json
import logging
import code_tokenize as ctok
import os

# To see an example of python opensearch sdk https://opensearch.org/docs/1.2/clients/python/

# region Helpers
def getConnectionDetails():
    connection = {}
    try:
        with open("connection.json", "r") as f:
            connection = json.load(f)
    except Exception as ex:
        logging.error(ex)
    
    for key in ["host", "username","password"]:
        if key not in connection:
            connection[key] = input(f"Enter {key}: ")
    
    connection['port'] = connection.get("port", 9200)

    try:
        with open("connection.json", "w") as f:
            json.dump(connection, f, indent=4)
    except Exception as ex:
        logging.error(ex)

    return connection

def getClientLocal():
    con = getConnectionDetails()
    # Create the client with SSL/TLS enabled, but hostname verification disabled.
    return OpenSearch(
        hosts = [{
            'host': con.get("host"),
            'port': con.get("port")
        }],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = (con.get("username"), con.get("password")) ,
        use_ssl = True,
        ssl_assert_hostname = False,
        ssl_show_warn = False
    )

def getClientEc2():
    # # TODO use boto3 instead of password in env vars
    # import boto3
    # from requests_aws4auth import AWS4Auth
    # my_region = os.environ['AWS_REGION']
    # service = 'es' 
    # credentials = boto3.Session().get_credentials()
    # awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, my_region, service, session_token=credentials.token)
    http_auth =  ('admin', os.getenv('OPENSEARCH_PASS'))

    return  OpenSearch(
        hosts=[{
            'host': os.getenv('OPENSEARCH_HOST'),
            'port': os.getenv('OPENSEARCH_PORT') or 443
        }],
        http_auth =  http_auth,
        http_compress = True,
        use_ssl = True,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
    )

def getClient():
    my_user = os.environ.get("USER")
    if "ec2" in my_user:
        return getClientEc2()
    else:
        return getClientLocal()
# endregion

class SnippetSearch:
    def __init__(self, client: OpenSearch = None, **kwargs) -> None:
        self.client = client if client else getClient()
        self.index = kwargs.get("index", "snippet-search")
        self.ensureIndex()

    def makeId(self, data):
        return hash(data) % (10**8)

    def tokenize(self, code, lang="javascript") -> str:
        # return code
        return " ".join([str(t) for t in ctok.tokenize(code,lang=lang,syntax_error="ignore")])

    def ensureIndex(self):
        if (not self.client.indices.exists(self.index)):
            logging.info('\nCreating index:')
            response = self.client.indices.create(self.index, body={
                'settings': {
                    'index': {
                        'number_of_shards': 1
                    }
                }
            })
            logging.info(response)
        return True
    
    def snippetToDoc(self, codeSnippet, lang="javascript"):
        snippetTok = self.tokenize(codeSnippet, lang=lang)
        return {
            'id': self.makeId(codeSnippet + lang),
            'language': lang,
            'snippet': codeSnippet,
            'snippetTok': snippetTok
        }

    def addSnippet(self, codeSnippet, lang="javascript"):
        response = self.client.index(
            index = self.index,
            body = self.snippetToDoc(codeSnippet, lang=lang),
            refresh = True
        )
        logging.info(response)
        return response

    def addSnippets(self, snippets=[], lang="javascript"):        
        data = [
            {
                '_op_type': 'index',
                '_index': self.index,
                '_refresh': True,
                '_source': self.snippetToDoc(snippet, lang=lang),
            } for snippet in snippets
        ]
        success, failed = helpers.bulk(self.client, data, max_retries=3)
        msg = f"success: {success}, failed: {failed}"
        logging.info(msg)
        return success, failed
    
    def findSnippets(self, query="", lang="javascript"):
        # Search for the document.
        queryTok = self.tokenize(query, lang=lang)
        response = self.client.search(
            body = {
                'size': 5,
                'query': {
                    'bool': {
                        'should': [
                            {
                                'multi_match': {
                                    'query': query,
                                    'fields': ['snippet','snippetTok'],
                                }
                            },
                            {
                                'multi_match': {
                                    'query': queryTok,
                                    'fields': ['snippet','snippetTok'],
                                }
                            }
                        ],
                        'filter': [
                            {
                                'term': {
                                    'language': lang
                                }
                            }
                        ]
                    }
                }
            },
            index = self.index
        )
        logging.info('\nSearch results:')
        logging.info(response)
        # This is so ugly
        return response, [
            doc.get("_source", {}).get("snippet")
            for doc in response.get('hits', {}).get('hits', []) 
            if doc.get("_score", 0) > 0
        ]

def getHistory():
    with open("../../data/history.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    # Set the logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s()] %(message)s',
        handlers=[
            logging.FileHandler('snippetsearch.log'),
            logging.StreamHandler() # Print log messages to the console
        ]
    )
    
    # getConnectionDetails()
    # client = getClient()
    # logging.info("Can access server?: %s", client.ping())

    ss = SnippetSearch()

    addRes = ss.addSnippets(getHistory().get("cam"))
    res, findRes = ss.findSnippets("Duration")

    logging.info("Found %s!", findRes)