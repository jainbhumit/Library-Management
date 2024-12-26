from fastapi import APIRouter,Request
from starlette import status

from src.app.controller.issue_book.handler import IssueBookHandler
from src.app.dto.issue_book import IssueBookDTO
from src.app.services.issue_book_service import IssueBookService

def create_issue_book_route(issue_book_service:IssueBookService):
    router = APIRouter(prefix="/book", tags=["issue_book"])
    issue_book_handler = IssueBookHandler.create(issue_book_service)

    @router.post("/issue-book",status_code=status.HTTP_201_CREATED)
    async def issue_book_by_user(request:Request,request_body:IssueBookDTO):
        return await issue_book_handler.issue_book_by_user(request,request_body)

    @router.patch("/return-book/{book_id}")
    async def return_book_by_user(book_id,request: Request):
        return await issue_book_handler.return_book_by_user(book_id,request)

    @router.get("/issue-book")
    async def get_issued_books(request: Request):
        return await issue_book_handler.get_issued_books(request)

    return router
