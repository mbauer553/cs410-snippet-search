from snippetsearch import snippetsearch
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s()] %(message)s',
    handlers=[
        logging.StreamHandler() # Print log messages to the console
    ]
)

ss = snippetsearch.SnippetSearch()

def lambda_handler(event, context):
    # Extract HTTP method and path from the API Gateway event
    http_method = event['httpMethod']
    path = event['path']

    if http_method == 'POST' or http_method == 'PUT':
        if path == '/addsnippet':
            # Handle /addsnippet endpoint
            return add_snippet(event)
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Invalid endpoint')
            }
    elif http_method == 'GET':
        if path == '/findsnippet':
            # Handle /findsnippet endpoint
            return find_snippet(event)
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Invalid endpoint')
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported HTTP method')
        }

def add_snippet(event):
    # Extract data from the request body
    try:
        request_body = json.loads(event['body'])
        snippet = request_body.get('snippet', '')
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON format in the request body')
        }

    # Process the snippet (in this case, just checking if it's not empty)
    if snippet:
        # Perform your processing here
        # ...
        ss.addSnippet(snippet)

        return {
            'statusCode': 200,
            'body': json.dumps(True)
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Snippet is required')
        }

def find_snippet(event):
    # Extract query parameters from the request
    params = event['queryStringParameters']
    snippet_to_find = params.get('snippet', '')
    lang = params.get('lang', 'javascript')

    # Process the snippet_to_find (in this case, just returning it in a list)
    if snippet_to_find:
        _, result = ss.findSnippets(snippet_to_find, lang=lang)

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Snippet parameter is required for /findsnippet')
        }
