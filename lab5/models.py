from database import book_collection
from schemas import BookSchema, BookDB
from bson import ObjectId
from pydantic_mongo import PydanticObjectId


async def get_books():
    books = []
    cursor = book_collection.find({})
    async for doc in cursor:
        books.append(BookDB(**doc))
    return books

async def get_book_by_id(book_id: str):
    return await book_collection.find_one({"_id": PydanticObjectId(book_id)})

async def add_book(book_data: BookSchema):
    book_dict = book_data.dict()
    result = await book_collection.insert_one(book_dict)
    return await get_book_by_id(result.inserted_id)

async def delete_book(book_id: str):
    result = await book_collection.delete_one({"_id": PydanticObjectId(book_id)})
    return result.deleted_count == 1
