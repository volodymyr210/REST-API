from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from models import get_books, get_book_by_id, add_book, delete_book
from schemas import BookSchema, BookDB

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    books = await get_books()
    return templates.TemplateResponse("book_main.html", {"request": request, "books": books})

@app.get("/books", response_model=List[BookDB])
async def read_books():
    return await get_books()

@app.get("/books/{book_id}", response_model=BookDB)
async def read_book(book_id: str):
    book = await get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@app.post("/books", response_model=BookDB, status_code=201)
async def create_book(book: BookSchema):
    return await add_book(book)

@app.delete("/books/{book_id}")
async def remove_book(book_id: str):
    deleted = await delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return {"message": "Книгу видалено"}
