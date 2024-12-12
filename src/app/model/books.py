import uuid


class Books:
    def __init__(self,title,author,no_of_copies=1,no_of_available=1,id=None):
        self.id = id if id else str(uuid.uuid4())
        self.title = title
        self.author = author
        self.no_of_copies = no_of_copies
        self.no_of_available = no_of_available