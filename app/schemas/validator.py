from datetime import datetime


def end_date_must_be_valid(end_date: str, start_date: str) -> str:
    if end_date:
        validate_date(end_date)

        if start_date and end_date < start_date:
            raise ValueError("End date must be greater than start date")
    return end_date


def start_date_must_be_valid(start_date: str) -> str:
    if start_date:
        validate_date(start_date)
    return start_date


def limit_must_be_valid(limit: int) -> int:
    if limit < 1:
        raise ValueError("Limit must be positive")
    elif limit > 100:
        raise ValueError("Limit must be less than 101")
    return limit


def validate_date(date_str: str) -> str:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            "Invalid date format: {date_str}. Required format YYYY-MM-DD."
        )
    return date_str
