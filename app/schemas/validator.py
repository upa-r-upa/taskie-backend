from datetime import datetime
from app.api.errors import (
    INVALID_VALUE_RANGE,
    START_DATE_GREATER_THAN_END_DATE,
)


def end_date_must_be_valid(end_date: datetime, start_date: datetime) -> str:
    if end_date:
        if start_date and end_date < start_date:
            raise ValueError(START_DATE_GREATER_THAN_END_DATE)
    return end_date


def limit_must_be_valid(limit: int) -> int:
    if limit < 1:
        raise ValueError(INVALID_VALUE_RANGE)
    elif limit > 100:
        raise ValueError(INVALID_VALUE_RANGE)
    return limit
