import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo_admin:password@mongo_db:27017")
db = client.books_db
book_collection = db.books
