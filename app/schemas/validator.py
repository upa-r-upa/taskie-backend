from datetime import datetime


def end_date_must_be_valid(end_date: str, start_date: str) -> str:
    if end_date:
        try:
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("End date must be in the format YYYY-MM-DD")
        if start_date and end_date < start_date:
            raise ValueError("End date must be greater than start date")
    return end_date


def start_date_must_be_valid(start_date: str) -> str:
    if start_date:
        try:
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Start date must be in the format YYYY-MM-DD")
    return start_date


def limit_must_be_valid(limit: int) -> int:
    if limit < 1:
        raise ValueError("Limit must be positive")
    elif limit > 100:
        raise ValueError("Limit must be less than 101")
    return limit
