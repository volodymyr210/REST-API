from bson import ObjectId
from database import book_collection

def get_all_books():
    return list(book_collection.find())

def get_book(book_id):
    return book_collection.find_one({"_id": ObjectId(book_id)})

def add_book(data):
    result = book_collection.insert_one(data)
    return get_book(result.inserted_id)

def delete_book(book_id):
    result = book_collection.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count == 1
