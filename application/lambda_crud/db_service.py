from book import Book
import boto3

class DBService():
    def __init__(self, table_name: str="Books"):
        self.table_name = table_name
        self.table =  boto3.resource('dynamodb').Table(self.table_name)
        
    def create_book(self, book: Book):
        return self.table.put_item(
        Item=vars(book)
        )

    def update_book(self, book: Book):
        return self.table.update_item(
            Keys=book.keys(),
            UpdateExpression=Book.update_expression,
            ExpressionAttributeValues=book.values()
        )

    def get_book(self, book: Book):
        return self.table.get_item(Item=book.keys())["Item"]

    def delete_book(self, book: Book):
        return self.table.delete_item(Key=book.keys())
