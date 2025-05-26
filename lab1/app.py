from flask import Flask, jsonify, request,render_template, url_for
from models import db, Book
from flask_migrate import Migrate
import os
from base64 import b64encode, b64decode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/library_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    return render_template("book_main.html")

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Книга не знайдена"}), 404
    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year
    })

@app.route('/books', methods=['GET'])
def get_books():
    cursor = request.args.get('cursor', None)
    page_size = request.args.get('page_size', 10, type=int)
    
    query = Book.query.order_by(Book.id)
    
    if cursor:
        try:
            last_id = int(b64decode(cursor.encode()).decode())
            query = query.filter(Book.id > last_id)
        except Exception:
            return jsonify({"error": "Невірний формат курсора"}), 400
    
    books = query.limit(page_size + 1).all()
    
    has_next = len(books) > page_size
    books = books[:page_size]
    
    response = {
        "books": [{"id": b.id, "title": b.title, "author": b.author, "year": b.year} for b in books],
        "has_next": has_next
    }
    
    if has_next and books:
        next_cursor = b64encode(str(books[-1].id).encode()).decode()
        response["next_cursor"] = next_cursor
    
    return jsonify(response)

@app.route('/books', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        book = Book(title=data['title'], author=data['author'], year=data['year'])
        db.session.add(book)
        db.session.commit()
        return jsonify({"id": book.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Книгу не знайдено"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Книгу видалено"})
