from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class BaseRequestModel(BaseModel):
    model_config = ConfigDict(
        extra='forbid',  # Prevent extra fields
        str_strip_whitespace=True,  # Automatically strip whitespace
        populate_by_name=True
    )

class IssueBookDTO(BaseRequestModel):
    book_id: str = Field(..., description="The ID of the book to be issued")
    return_date: date = Field(..., description="The date the book is to be returned (YYYY-MM-DD)")
