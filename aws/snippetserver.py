from flask import Flask, request, jsonify
from snippetsearch import snippetsearch
import json
import logging

app = Flask(__name__)
ss = snippetsearch.SnippetSearch()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s()] %(message)s',
    handlers=[
        logging.StreamHandler()  # Print log messages to the console
    ]
)

@app.route('/addsnippet', methods=['POST', 'PUT'])
def add_snippet():
    try:
        request_body = request.get_json()
        snippet = request_body.get('snippet', '')
    except json.JSONDecodeError:
        return jsonify({'statusCode': 400, 'body': 'Invalid JSON format in the request body'})

    if snippet:
        # Perform your processing here
        # ...
        ss.addSnippet(snippet)

        return jsonify({'statusCode': 200, 'body': True})
    else:
        return jsonify({'statusCode': 400, 'body': 'Snippet is required'})

@app.route('/findsnippet', methods=['GET'])
def find_snippet():
    params = request.args
    snippet_to_find = params.get('snippet', '')
    lang = params.get('lang', 'javascript')

    if snippet_to_find:
        _, result = ss.findSnippets(snippet_to_find, lang=lang)

        return jsonify({'statusCode': 200, 'body': result})
    else:
        return jsonify({'statusCode': 400, 'body': 'Snippet parameter is required for /findsnippet'})

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app locally in debug mode
