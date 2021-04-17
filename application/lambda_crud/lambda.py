import json

from book import Book
from db_service import DBService

db_service = DBService()

strategy = {
    "POST":db_service.create_book ,
    "PUT": db_service.update_book,
    "GET": db_service.get_book,
    "DELETE": db_service.delete_book,
}


def handler(event, _):
    body = json.loads(event["body"])
    book = create_book(body)
    strategy.get(event.get("http").get("method"))(book)

def create_book(body):
    author = body["author"]
    title = body["title"]
    description = body.get("description")
    return Book(author=author, title=title, description=description)
