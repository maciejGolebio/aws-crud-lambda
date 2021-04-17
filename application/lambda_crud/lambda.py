import json
import os

from book import Book
from db_service import DBService

TABLE_NAME = os.environ.get('TABLE', "books")
db_service = DBService(TABLE_NAME)

strategy = {
    "POST": db_service.create_book,
    "PUT": db_service.update_book,
    "GET": db_service.get_book,
    "DELETE": db_service.delete_book,
}


def handler(event, _):
    body = json.loads(event["body"])
    book = create_book(body)
    resp = strategy.get(event.get("httpMethod"))(book)
    return {
        "statusCode": 200,
        "body": resp
    }


def create_book(body):
    author = body["author"]
    title = body["title"]
    description = body.get("description")
    return Book(author=author, title=title, description=description)
