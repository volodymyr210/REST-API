from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField

class BookSchema(BaseModel):
    title: str
    author: str
    year: int

class BookDB(BookSchema):
    id: ObjectIdField = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True  # щоб можна було ініціалізувати з _id
        json_encoders = {
            ObjectIdField: str  # Конвертація ObjectId у рядок при серіалізації
        }
