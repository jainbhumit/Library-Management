from src.app.model.issued_books import IssuedBooks
from src.app.utils.db.db import DB
from src.app.utils.errors.error import DatabaseError
from src.app.utils.db.query import GenericQueryBuilder
class IssuedBookRepository:
    def __init__(self,db:DB):
        self.db = db

    def save_issue_book(self,issue_book:IssuedBooks):
        try:
            conn = self.db.get_connection()
            with conn:
                query,value = GenericQueryBuilder.insert("issuedBook",{
                    "id":issue_book.id,
                    "user_id":issue_book.user_id,
                    "book_id":issue_book.book_id,
                    "borrow_date":issue_book.borrow_date,
                    "return_date":issue_book.return_date,
                })
                conn.execute(query,value)
        except Exception as e:
            raise DatabaseError(str(e))

    def remove_issue_book(self,user_id:str,book_id:str):
        try:
            conn = self.db.get_connection()
            with conn:
                query,value = GenericQueryBuilder.delete("issuedBook",{
                    "user_id":user_id,
                    "book_id":book_id,
                })
                conn.execute(query,value)
        except Exception as e:
            raise DatabaseError(str(e))

    def get_issue_books(self,limit:int=100):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query,value = GenericQueryBuilder.select("issuedBook",[
                    "id",
                    "user_id",
                    "book_id",
                    "borrow_date",
                    "return_date",
                ],limit=limit)
                cursor.execute(query,value)
                results = cursor.fetchall()
                return [
                    IssuedBooks(id=row[0],user_id=row[1],book_id=row[2],borrow_date=row[3],return_date=row[4])
                    for row in results
                ] if results else []
        except Exception as e:
            raise DatabaseError(str(e))

    def get_issue_book_by_user_id(self,user_id:str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query,value = GenericQueryBuilder.select("issuedBook",[
                    "id",
                    "user_id",
                    "book_id",
                    "borrow_date",
                    "return_date",
                ],{"user_id":user_id})
                cursor.execute(query,value)
                results = cursor.fetchall()
                return [
                    IssuedBooks(id=row[0],user_id=row[1],book_id=row[2],borrow_date=row[3],return_date=row[4])
                    for row in results
                ] if results else []
        except Exception as e:
            raise DatabaseError(str(e))



