import uuid


class IssuedBooks:
    def __init__(self,user_id,book_id,borrow_date,return_date,id=None):
        self.id = id if id else str(uuid.uuid4())
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.return_date = return_date
