
def get_books():
    return books

def get_book_by_id(book_id):
    return next((book for book in books if book["id"] == book_id), None)

def add_book(book_data):
    books.append(book_data)
    return book_data

def delete_book(book_id):
    global books
    book_to_delete = get_book_by_id(book_id)
    if book_to_delete:
        books = [book for book in books if book["id"] != book_id]
        return True
    return False
