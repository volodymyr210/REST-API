
books = [
    {"id": 1, "title": "book1", "author": "George Orwell", "year": 1949},
    {"id": 2, "title": "book2", "author": "Harper Lee", "year": 1960}
]
next_id = 3

def get_all_books():
    return books

def get_book_by_id(book_id):
    return next((book for book in books if book["id"] == book_id), None)

def add_book(data):
    global next_id
    data["id"] = next_id
    next_id += 1
    books.append(data)
    return data

def delete_book(book_id):
    global books
    book = get_book_by_id(book_id)
    if book:
        books.remove(book)
        return True
    return False
