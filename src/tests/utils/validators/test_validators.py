import unittest

from src.app.utils.validators.validators import Validators


class TestValidators(unittest.TestCase):

    def test_is_name_valid(self):
        # Valid names
        self.assertTrue(Validators.is_name_valid("Alice"))
        self.assertTrue(Validators.is_name_valid("Bob"))
        # Invalid names
        self.assertFalse(Validators.is_name_valid("A"))  # Too short
        self.assertFalse(Validators.is_name_valid("ThisNameIsTooLong"))  # Too long

    def test_is_email_valid(self):
        # Valid emails
        self.assertTrue(Validators.is_email_valid("example@jecrc.ac.in"))
        self.assertTrue(Validators.is_email_valid("user123@jecrc.ac.in"))
        # Invalid emails
        self.assertFalse(Validators.is_email_valid("example@yahoo.com"))  # Non-Gmail
        self.assertFalse(Validators.is_email_valid("user@gmail"))  # Missing .com
        self.assertFalse(Validators.is_email_valid("user123@.com"))  # Invalid domain
        self.assertFalse(Validators.is_email_valid("user@gmail.com"))

    def test_is_password_valid(self):
        # Valid passwords
        self.assertTrue(Validators.is_password_valid("Password@123"))
        self.assertTrue(Validators.is_password_valid("Strong#Pass8"))
        # Invalid passwords
        self.assertFalse(Validators.is_password_valid("short"))  # Too short
        self.assertFalse(Validators.is_password_valid("nouppercase@123"))  # No uppercase
        self.assertFalse(Validators.is_password_valid("NOLOWERCASE@123"))  # No lowercase
        self.assertFalse(Validators.is_password_valid("NoSpecialChar123"))  # No special character

    def test_is_year_valid(self):
        # Valid year
        self.assertTrue(Validators.is_year_valid("1"))
        self.assertTrue(Validators.is_year_valid("2"))
        self.assertTrue(Validators.is_year_valid("4"))
        self.assertTrue(Validators.is_year_valid("1st"))
        self.assertTrue(Validators.is_year_valid("2nd"))
        self.assertTrue(Validators.is_year_valid("3rd"))
        self.assertTrue(Validators.is_year_valid("4th"))

        # Invalid year
        self.assertFalse(Validators.is_year_valid("0"))
        self.assertFalse(Validators.is_year_valid("5"))
        self.assertFalse(Validators.is_year_valid("5th"))
        self.assertFalse(Validators.is_year_valid("1bf"))









