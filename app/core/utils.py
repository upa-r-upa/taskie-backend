from datetime import datetime
from typing import Optional

from app.api.errors import INVALID_DATE_FORMAT


def validate_date_format(date_str: Optional[str]) -> Optional[str]:
    if date_str:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(INVALID_DATE_FORMAT)
    return date_str
