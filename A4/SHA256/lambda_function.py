import hashlib
import json
import urllib.request

def lambda_handler(event, context):
    value = event['value']
    
    # Perform sha256 hashing
    hashed_value = hashlib.sha256(value.encode('utf-8')).hexdigest()
    
    # response to be sent back to the course -uri
    response = {
        "banner": "B00931943",
        "result": hashed_value,
        "arn": "arn:aws:lambda:us-east-1:704579266563:function:SHA-265",
        "action": "sha256",
        "value": value
    }
    
    response_course_uri(event['course_uri'], response)
    
    # return response

def response_course_uri(url, data):
    request = urllib.request.Request(url, method='POST')
    request.add_header('Content-Type', 'application/json')
    
    with urllib.request.urlopen(request, json.dumps(data).encode('utf-8')) as response:
        pass
