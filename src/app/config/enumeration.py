from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class Branch(Enum):
    IT = 'INFORMATION TECHNOLOGY'
    CS = 'COMPUTER SCIENCE'
    ME = 'MECHANICAL ENGINEERING'
    EE = 'ELECTRICAL ENGINEERING'
    CE = 'CIVIL ENGINEERING'


class Status(Enum):
    SUCCESS = "success"
    FAIL = "fail"