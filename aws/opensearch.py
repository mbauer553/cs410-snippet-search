from opensearchpy import OpenSearch
import json
import logging

# Set the logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s()] %(message)s',
    handlers=[
        logging.FileHandler('opensearch.log'),
        logging.StreamHandler() # Print log messages to the console
    ]
)

# region Example
# comes from https://opensearch.org/docs/1.2/clients/python/
def sample(client, cleanup=True):
    # Create an index with non-default settings.
    index_name = 'python-test-index'
    index_body = {
        'settings': {
            'index': {
                'number_of_shards': 4
            }
        }
    }

    response = client.indices.create(index_name, body=index_body)
    logging.info('\nCreating index:')
    logging.info(response)

    # Add a document to the index.
    document = {
        'title': 'Moneyball',
        'director': 'Bennett Miller',
        'year': '2011'
    }
    id = '1'

    response = client.index(
        index = index_name,
        body = document,
        id = id,
        refresh = True
    )

    logging.info('\nAdding document:')
    logging.info(response)

    # Search for the document.
    q = 'miller'
    query = {
    'size': 5,
    'query': {
        'multi_match': {
        'query': q,
        'fields': ['title^2', 'director']
        }
    }
    }

    response = client.search(
        body = query,
        index = index_name
    )
    logging.info('\nSearch results:')
    logging.info(response)

    if (not cleanup):
        return
    
    sampleCleanup(client, index_name, id)

def sampleCleanup(client, index_name = 'python-test-index', id = '1'):
    # Delete the document.
    response = client.delete(
        index = index_name,
        id = id
    )

    logging.info('\nDeleting document:')
    logging.info(response)

    # Delete the index.
    response = client.indices.delete(
        index = index_name
    )

    logging.info('\nDeleting index:')
    logging.info(response)
# endregion

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

def getClient():
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

# endregion

class SnippetSearch:
    def __init__(self, client: OpenSearch, **kwargs) -> None:
        self.client = client
        self.index = kwargs.get("index", "snippet-search")
        self.ensureIndex()

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

    def addSnippet(self, codeSnippet, language="js"):
        response = self.client.index(
            index = self.index,
            body = {
                'language': language,
                'snippet': codeSnippet
            },
            refresh = True
        )
        logging.info(response)
        return response

    def addSnippets(self, codeSnippsets=[], language="js"):
        raise NotImplementedError('bulk snippets not implemented yet')
    
    def findSnippets(self, queryText="", language="js"):
        # Search for the document.
        query = {
            'size': 5,
            'query': {
                'bool': {
                    'must': [
                        {
                            'match': {
                                'snippet': queryText,
                            }
                        },
                        {
                            'term': {
                                'language': language
                            }
                        }
                    ]
                }
            }
        }

        response = self.client.search(
            body = query,
            index = self.index
        )
        logging.info('\nSearch results:')
        logging.info(response)
        # This is so ugly
        return list(map(lambda x: x.get("_source", {}).get("snippet"), response.get('hits', {}).get('hits', [])))

if __name__ == "__main__":
    # getConnectionDetails()
    client = getClient()
    logging.info("Can access server?: %s", client.ping())

    ss = SnippetSearch(client)

    addRes1 = ss.addSnippet("Duration.fromString(\"24h24m\").milliseconds()")
    addRes2 = ss.addSnippet("Duration.fromString(\"24h24m\").milliseconds() Duration test")
    findRes = ss.findSnippets("Duration")

    logging.info("Found %s!", findRes)