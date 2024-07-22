from datetime import datetime

from app.api.errors import (
    INVALID_DATE_FORMAT,
    INVALID_VALUE_RANGE,
    START_DATE_GREATER_THAN_END_DATE,
)


def end_date_must_be_valid(end_date: str, start_date: str) -> str:
    if end_date:
        validate_date(end_date)

        if start_date and end_date < start_date:
            raise ValueError(START_DATE_GREATER_THAN_END_DATE)
    return end_date


def start_date_must_be_valid(start_date: str) -> str:
    if start_date:
        validate_date(start_date)
    return start_date


def limit_must_be_valid(limit: int) -> int:
    if limit < 1:
        raise ValueError(INVALID_VALUE_RANGE)
    elif limit > 100:
        raise ValueError(INVALID_VALUE_RANGE)
    return limit


def validate_date(date_str: str) -> str:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(INVALID_DATE_FORMAT)
    return date_str
