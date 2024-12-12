from src.app.model.books import Books
from src.app.utils.db.db import DB
from src.app.utils.db.query import GenericQueryBuilder
from src.app.utils.errors.error import DatabaseError
class BooksRepository:
    def __init__(self,db:DB) -> None:
        self.db = db

    def add_book(self,book:Books):
        try:
            conn = self.db.get_connection()
            with conn:
                query,value = GenericQueryBuilder.insert("book",{
                    "id":book.id,
                    "title":book.title,
                    "author":book.author,
                    "number_of_copies":book.no_of_copies,
                    "number_of_available_books":book.no_of_available
                })
                conn.execute(query,value)
        except Exception as e:
            raise DatabaseError(str(e))

    def update_book(self,book:Books):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query,value = GenericQueryBuilder.update("book",{
                    "title":book.title,
                    "author":book.author,
                },{"id":book.id})
                cursor.execute(query,value)
        except Exception as e:
            raise DatabaseError(str(e))

    def delete_book(self,book_id:str):
        try:
            conn = self.db.get_connection()
            with conn:
                query,value = GenericQueryBuilder.delete("book",{"id":book_id})
                conn.execute(query,value)
        except Exception as e:
            raise DatabaseError(str(e))

    def get_books(self,limit:int=100):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query,value = GenericQueryBuilder.select("book",[
                    "id",
                    "title",
                    "author",
                    "number_of_copies",
                    "number_of_available_books",
                ],limit=limit)
                if value:
                    cursor.execute(query,value)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                return [Books(id=row[0],
                              title=row[1],
                              author=row[2],
                              no_of_copies=row[3],
                              no_of_available=row[4]
                              ) for row in results] if results else []
        except Exception as e:
            raise DatabaseError(str(e))

    def get_book_by_title(self,title:str):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query,value = GenericQueryBuilder.select("book",[
                    "id",
                    "title",
                    "author",
                    "number_of_copies",
                    "number_of_available_books",
                ],{"title":title})
                cursor.execute(query,value)
                result = cursor.fetchone()
                if result:
                    return Books(id=result[0],title=result[1],author=result[2],no_of_copies=result[3],no_of_available=result[4])
                else:
                    return None
        except Exception as e:
            raise DatabaseError(str(e))

    def update_book_availability(self,book:Books):
        try:
            conn = self.db.get_connection()
            with conn:
                query,value = GenericQueryBuilder.update("book",{
                    "number_of_copies":book.no_of_copies,
                    "number_of_available_books":book.no_of_available,
                },{"title":book.title})
                conn.execute(query,value)
        except Exception as e:
            raise DatabaseError(str(e))

    def get_book_by_id(self,id:str,limit:int=100):
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query,value = GenericQueryBuilder.select("book",[
                    "id",
                    "title",
                    "author",
                    "number_of_copies",
                    "number_of_available_books",
                ],{"id":id},limit=limit)
                cursor.execute(query,value)
                result = cursor.fetchone()
                if result:
                    return Books(id=result[0],title=result[1],author=result[2],no_of_copies=result[3],no_of_available=result[4])
                else:
                    return None
        except Exception as e:
            raise DatabaseError(str(e))


def new_books_repository(db):
    return BooksRepository(db)
