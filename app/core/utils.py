from datetime import datetime
from typing import Optional

from app.api.errors import INVALID_DATE_FORMAT


def validate_date_format(date_str: Optional[str]) -> Optional[datetime]:
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(INVALID_DATE_FORMAT)
    return None
