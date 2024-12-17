import re
import uuid
from src.app.config.enumeration import Role, Branch


class Validators:

    @staticmethod
    def is_name_valid(name: str) -> bool:
        """
        Validate if the given name is valid (2 < len < 16).
        :param name:
        :return:
        """
        return 2 < len(name) < 16

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """
        Validate if the given email is a valid Gmail account.
        :param email:
        :return:
        """
        gmail_regex = r"^[a-zA-Z0-9._%+-]+@jecrc.ac\.in$"
        return bool(re.match(gmail_regex, email))

    @staticmethod
    def is_password_valid(password: str) -> bool:
        """
        Validate if the given password meets the required criteria:
        - Length between 8 and 16 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one special character
        """
        if not (8 <= len(password) <= 16):
            return False

        upper_case = False
        lower_case = False
        special_char = False

        # Define a set of special characters
        special_characters = set("!@#$%^&*()-_=+[]{}|;:',.<>?/")

        for char in password:
            if char.isupper():
                upper_case = True
            elif char.islower():
                lower_case = True
            elif char in special_characters:
                special_char = True

        return upper_case and lower_case and special_char

    @staticmethod
    def is_year_valid(year: str) -> bool:
        if year in ('1','2','3','4','1st','2nd','3rd','4th'):
            return True
        return False

    @staticmethod
    def is_branch_valid(branch: str) -> bool:
        return branch.upper() in Branch.__members__

    @staticmethod
    def is_valid_role(role:str):
        if role.lower() == Role.USER.value:
            return True
        return False

