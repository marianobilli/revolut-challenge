import pytest
import requests

from api import days_till_birthday, birthday_message, validate_request
from datetime import datetime, timedelta


def test_days_till_birthday():
    assert days_till_birthday(datetime.now().date().replace(year=1980)) == 0
    assert days_till_birthday(datetime.now().date().replace(year=1980)+timedelta(days=10)) == 10

def test_birthday_message():
    days = 10
    assert birthday_message(datetime.now().date().replace(year=1980)) == "Happy birthday!"
    assert birthday_message(datetime.now().date().replace(year=1980)+timedelta(days=days)) == f"Your birthday is in {days} day(s)"

def test_validate_request_username_length():
    with pytest.raises(Exception):
        assert validate_request(username="12345678901234567890123456")