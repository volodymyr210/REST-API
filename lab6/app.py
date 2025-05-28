from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource
from flasgger import Swagger
from models import get_all_books, get_book, add_book, delete_book
from schemas import BookSchema

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

@app.route("/")
def index():
    return render_template("book_main.html")

class BookListResource(Resource):
    def get(self):
        """
        Отримати список книг
        ---
        responses:
          200:
            description: Список книг
        """
        books = get_all_books()
        for b in books:
            b["id"] = str(b["_id"])
        return book_list_schema.dump(books), 200

    def post(self):
        """
        Додати нову книгу
        ---
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: Book
              required:
                - title
                - author
                - year
              properties:
                title:
                  type: string
                author:
                  type: string
                year:
                  type: integer
        responses:
          201:
            description: Книга створена
        """
        data = request.json
        new_book = add_book(data)
        new_book["id"] = str(new_book["_id"])
        return book_schema.dump(new_book), 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Книга знайдена
          404:
            description: Книга не знайдена
        """
        book = get_book(book_id)
        if not book:
            return {"message": "Книгу не знайдено"}, 404
        book["id"] = str(book["_id"])
        return book_schema.dump(book), 200

    def delete(self, book_id):
        """
        Видалити книгу
        ---
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Книгу видалено
          404:
            description: Книгу не знайдено
        """
        success = delete_book(book_id)
        if not success:
            return {"message": "Книгу не знайдено"}, 404
        return {"message": "Книгу видалено"}, 200

api.add_resource(BookListResource, "/books")
api.add_resource(BookResource, "/books/<string:book_id>")

if __name__ == "__main__":
    app.run(debug=True)
