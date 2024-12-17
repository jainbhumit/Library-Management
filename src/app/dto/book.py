from pydantic import BaseModel, Field, ConfigDict


class BaseRequestModel(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        populate_by_name=True
    )

class CreateBookDTO(BaseRequestModel):
    title: str = Field(...,description="Title of the book")
    author: str = Field(..., description="Author of the book")

class UpdateBookDTO(BaseRequestModel):
    book_id: str = Field(..., description="ID of the book to update")
    title: str = Field(..., description="Updated title of the book")
    author: str = Field(..., description="Updated author of the book")
