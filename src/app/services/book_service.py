from src.app.config.messages import BOOK_NOT_EXIST
from src.app.repositories.books_repository import BooksRepository
from src.app.model.books import Books
from src.app.utils.errors.error import *


class BookService:
    def __init__(self,book_repository:BooksRepository):
        self.book_repository = book_repository

    def __repr__(self):
        print(f"<class: Bookservice>")
        pass

    def add_book(self,new_book:Books):
        book = self.book_repository.get_book_by_title(new_book.title)
        if book is None:
            self.book_repository.add_book(new_book)
        else:
            book.no_of_available=book.no_of_available + 1
            book.no_of_copies= book.no_of_copies + 1
            self.book_repository.update_book_availability(book)

    def update_book_by_id(self,updated_book:Books,book_id:str):
        if self.book_repository.get_book_by_id(book_id) is None:
            raise NotExistsError(BOOK_NOT_EXIST)

        updated_book.id=book_id
        self.book_repository.update_book(updated_book)

    def remove_all_book_by_id(self,book_id:str):
        if self.book_repository.get_book_by_id(book_id) is None:
            raise NotExistsError(BOOK_NOT_EXIST)

        self.book_repository.delete_book(book_id)

    def remove_book_by_id(self,book_id:str):
        book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            raise NotExistsError(BOOK_NOT_EXIST)

        book.no_of_available-=1
        book.no_of_copies-=1
        self.book_repository.update_book_availability(book)


    def get_all_books(self):
        books = self.book_repository.get_books()
        return books


    def get_book_by_title(self,title:str):
        book = self.book_repository.get_book_by_title(title)
        if book is None:
            raise NotExistsError(BOOK_NOT_EXIST)
        return book







