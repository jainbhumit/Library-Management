from http import HTTPStatus

from fastapi import APIRouter,Request
from starlette import status

from src.app.controller.book.handler import BookHandler
from src.app.dto.book import CreateBookDTO, UpdateBookDTO
from src.app.services.book_service import BookService


def create_book_route(book_service:BookService):
    router = APIRouter()
    book_handler = BookHandler(book_service)

    @router.post("/admin/book",status_code=status.HTTP_201_CREATED)
    async def create_book(request:Request,request_body:CreateBookDTO):
        return await book_handler.create_book(request,request_body)

    @router.put("/admin/book")
    async def update_book(request: Request, request_body: UpdateBookDTO):
        return await book_handler.update_book(request, request_body)

    @router.patch("/admin/book/{book_id}")
    async def remove_book(book_id:str,request: Request):
        return await book_handler.remove_book(book_id,request)

    @router.delete("/admin/book/{book_id}")
    async def delete_book(book_id:str,request: Request):
        return await book_handler.delete_book(book_id,request)

    @router.get("/user/book")
    async def get_all_books(request:Request):
        return await book_handler.get_all_books(request)


    return router



