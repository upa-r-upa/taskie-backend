from datetime import datetime
from typing import Optional

def validate_date_format(date_str: Optional[str]) -> Optional[datetime]:
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                detail=f"Invalid date format: {date_str}. Required format YYYY-MM-DD.",
            )
    return None
