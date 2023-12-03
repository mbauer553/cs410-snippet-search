# How this works 

## snippet search 
snippetsearch is a module with basic code to either addSnippets or findSnippets. Internally, it will parse the snippet using code_tokenize which works for python, javascript, or a range of other languages. 

The output of this, along with the original snippet, is stored in an index called "snippet-search".

Then, when a snippet is searched, we query that index for anything matching the query or the parsed query (using code_tokenize again).

Right now, the limit returned is a max of 5. No results will be returned if there are no quality matches.

## snippet server
To serve requests, we have snippet server which is just a flask wrapper on snippet search to serve requests over rest. 

/addsnippet POST/PUT 
{
  "snippet": "your_snippet_here",
  "language": "javascript" # python, others
}

/findSnippets GET
snippet=your_search_snippet&lang=javascript


## Connection details

ec2 instance running: 

host: ec2-23-20-145-210.compute-1.amazonaws.com
port: 8080

## Examples

```
curl -X POST -H "Content-Type: application/json" -d '{"snippet": "Duration.fromString(\"24h\")"}' http://ec2-23-20-145-210.compute-1.amazonaws.com:8080/addsnippet

{
  "body": true,
  "statusCode": 200
}
```

```
curl -X GET "http://ec2-23-20-145-210.compute-1.amazonaws.com:8080/findsnippet?snippet=Duration&lang=javascript"

{
  "body": [
    "Duration",
    "c3Make(\"Duration\", {ms: 1000})",
    "c3Make(\"Duration\", {m_ms: 1000})",
    "c3Make(\"Duration\", {ms: 1000})",
    "c3Make(\"Duration\", {m_ms: 1000})"
  ],
  "statusCode": 200
}
```