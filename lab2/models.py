
from typing import List, Optional

books = [
    {"id": 1, "title": "book1", "author": "George Orwell", "year": 1949},
    {"id": 2, "title": "book2", "author": "Harper Lee", "year": 1960}
]

next_id = 3  


def get_books() -> List[dict]:
    return books


def get_book_by_id(book_id: int) -> Optional[dict]:
    return next((book for book in books if book["id"] == book_id), None)


def add_book(book_data: dict) -> dict:
    global next_id
    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in book_data or not book_data[field]:
            raise ValueError(f"Поле '{field}' є обов'язковим і не може бути порожнім.")

    book_data["id"] = next_id
    next_id += 1
    books.append(book_data)
    return book_data



def delete_book(book_id: int) -> bool:
    global books
    book = get_book_by_id(book_id)
    if book:
        books = [b for b in books if b["id"] != book_id]
        return True
    return False
