from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from models import books, get_book_by_id, add_book, delete_book
from schemas import BookSchema

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("book_main.html", {"request": request, "books": books})

@app.get("/books")
async def get_books():
    return books

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@app.post("/books", status_code=201)
async def create_book(book: BookSchema):
    try:
        return add_book(book.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    global books
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(i)
            return {"message": "Книгу видалено"}
    raise HTTPException(status_code=404, detail="Книгу не знайдено")
