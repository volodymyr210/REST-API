from flask import Flask, jsonify, request, render_template
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)

books = [
    {"id": 1, "title": "book1", "author": "George Orwell", "year": 1949},
    {"id": 2, "title": "book2", "author": "Harper Lee", "year": 1960}
]
next_id = 3

class BookSchema(Schema):
    title = fields.String(required=True)
    author = fields.String(required=True)

book_schema = BookSchema()

@app.route("/")
def index():
    return render_template("book_main.html")

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book)
    return jsonify({"message": "Книгу не знайдено"}), 404

@app.route("/books", methods=["POST"])
def add_book():
    global next_id
    try:
        data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    data["id"] = next_id
    next_id += 1
    books.append(data)
    return jsonify(data), 201

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return jsonify({"message": "Книгу видалено"})
    return jsonify({"message": "Книгу не знайдено"}), 404

if __name__ == "__main__":
    app.run(debug=True)
