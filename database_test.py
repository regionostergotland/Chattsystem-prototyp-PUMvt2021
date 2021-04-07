import pytest
import database as DB

# Create database
DB.init()

"""
Test adding and deleteing keywords
"""
def test_keyword():
    DB.add_keyword("HEJ")
    assert DB.is_keyword("HEJ")

    DB.delete_keyword("HEJ")
    assert not DB.is_keyword("HEJ")
