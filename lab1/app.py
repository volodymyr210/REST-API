from flask import Flask, jsonify, request, render_template
from marshmallow import ValidationError
from models import get_all_books, get_book_by_id, add_book, delete_book
from schemas import BookSchema

app = Flask(__name__)
book_schema = BookSchema()

@app.route("/")
def index():
    return render_template("book_main.html")

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(get_all_books())

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = get_book_by_id(book_id)
    if book:
        return jsonify(book)
    return jsonify({"message": "Книгу не знайдено"}), 404

@app.route("/books", methods=["POST"])
def create_book():
    try:
        data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    new_book = add_book(data)
    return jsonify(new_book), 201

@app.route("/books/<int:book_id>", methods=["DELETE"])
def remove_book(book_id):
    if delete_book(book_id):
        return jsonify({"message": "Книгу видалено"})
    return jsonify({"message": "Книгу не знайдено"}), 404

if __name__ == "__main__":
    app.run(debug=True)
