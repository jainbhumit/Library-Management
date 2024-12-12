from typing import Optional

from src.app.utils.db.db import DB
from src.app.utils.db.query import GenericQueryBuilder
from src.app.model.user import User
from src.app.utils.errors.error import DatabaseError

class UserRepository:
    def __init__(self,db:DB):
        self.db = db

    def save_user(self,user:User):
        try:
            conn = self.db.get_connection()
            with conn:
                query,value = GenericQueryBuilder.insert("user",{
                    "id":user.id,
                    "name":user.name,
                    "email":user.email,
                    "role":user.role,
                    "year":user.year,
                    "branch":user.branch,
                    "password":user.password,
                })
                conn.execute(query,value)
        except Exception as e:
            raise DatabaseError(str(e))

    def fetch_user_by_email(self, email: str) -> Optional[User]:
        """Fetches a user from the database by their email."""
        try:
            conn = self.db.get_connection()
            with conn:
                cursor = conn.cursor()
                query,value = GenericQueryBuilder.select("user",
                                                        ["id","name","role","year","branch","email","password"],
                                                         {"email":email})
                cursor.execute(query,value)
                result = cursor.fetchone()

            if result:
                return User(
                    id=result[0],
                    name=result[1],
                    role=result[2],
                    year=result[3],
                    branch=result[4],
                    email=result[5],
                    password=result[6],
                )
            return None
        except Exception as e:
            raise DatabaseError(str(e))

    def delete_user_by_id(self,user_id:str):
        try:
            conn = self.db.get_connection()
            with conn:
                query,value = GenericQueryBuilder.delete("user",{"id":user_id})
                conn.execute(query,value)
        except Exception as e:
            raise DatabaseError(str(e))





def new_user_repository(db):
    return UserRepository(db)