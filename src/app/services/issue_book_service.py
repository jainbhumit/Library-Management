from src.app.repositories.issued_book_repository import IssuedBookRepository
from src.app.repositories.books_repository import BooksRepository
from src.app.model.issued_books import IssuedBooks
from src.app.utils.errors.error import *

class IssueBookService:
    def __init__(self,issued_book_repository:IssuedBookRepository,book_repository:BooksRepository):
        self.issued_book_repository = issued_book_repository
        self.book_repository = book_repository

    def get_all_issued_books(self):
        issued_books = self.issued_book_repository.get_issue_books()
        return issued_books


    def issue_book(self,issued_book:IssuedBooks,book_id:str):
        book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            raise NotExistsError("book doesn't exist")
        if book.no_of_available <= 0:
            raise InvalidOperationError("book doesn't available")
        issued_book.book_id = book.id
        self.issued_book_repository.save_issue_book(issued_book)
        book.no_of_available -= 1
        self.book_repository.update_book_availability(book)


    def return_issue_book(self,user_id:str,book_id:str):
        book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            raise NotExistsError("book doesn't exist")

        book.no_of_available +=1
        self.book_repository.update_book_availability(book)
        self.issued_book_repository.remove_issue_book(user_id,book_id)

    def get_issue_book_by_user_id(self,user_id:str):
        issued_books = self.issued_book_repository.get_issue_book_by_user_id(user_id)
        return issued_books


