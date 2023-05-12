import logging
import json
import boto3

_dynamodb = boto3.client('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name="books"

def get_book(book_id):
    return _dynamodb.query(
        ExpressionAttributeValues={ ':v1': { 'S': book_id }},
        KeyConditionExpression='book_name = :v1',
        TableName=table_name)

def create_book(book_data):
    return _dynamodb.put_item(
            TableName=table_name,
            Item={ "book_name": { "S": book_data['name'] }})

def update_book(book_id, book_data):
    return _dynamodb.update_item(
            TableName=table_name,
            Key={ "book_name": { "S": book_id }},
            UpdateExpression="set author = :r",
            ExpressionAttributeValues={ ':r': { "S": book_data['author'] }},
            ReturnValues="UPDATED_NEW")

def delete_book(book_id):
    return _dynamodb.delete_item(
            TableName=table_name,
            Key={ "book_name": { "S": book_id }})

def build_response(code, body):
    return {
        "statusCode": code,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps(body)
    }

def route(path, method, payload=None):
    if path.startswith("/books") and method == "GET":
        book_id = path.split('/')[2]
        response = build_response(200, get_book(book_id))
    elif path.startswith("/books") and method == "POST":
        response = build_response(201, create_book(payload))
    elif path.startswith("/books") and method == "PUT":
        book_id = path.split('/')[2]
        response = build_response(200, update_book(book_id, payload))
    elif path.startswith("/books") and method == "DELETE":
        book_id = path.split('/')[2]
        response = build_response(204, delete_book(book_id))
    else:
        raise Exception("unimplemented HTTP method error")

    return response

def handler(event, context):
    try:
        payload = json.loads(event['body'] or "{}")
        response = route(event['path'], event['httpMethod'], payload)
    except Exception as e:
        code = 500
        message = str(e)

        if message == "unimplemented HTTP method error":
            code = 400

        response = build_response(code, { "error": message })

    return response

