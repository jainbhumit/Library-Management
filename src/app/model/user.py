import uuid
from src.app.config.types import Role


class User:
    def __init__(self,name,year,branch,email,password,id=None,role=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.name = name
        self.role = Role.USER.value if role is None else role
        self.year = year
        self.branch = branch
        self.email = email
        self.password = password

