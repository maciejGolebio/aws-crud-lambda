class Book():
    ListAttributes = ["author", "title", "description"]

    @staticmethod
    def update_expression():
        return "set author=:a, title=:t, description=:d"

    def __init__(self, author, title, description=None):
        self.author = author
        self.title = title
        self.description = description

    def keys(self):
        return {
            "author": self.author,
            "title": self.title
        }

    def update_value(self):
        return {
            ":a": self.author,
            ":t": self.title,
            ":d": self.description,
        }
