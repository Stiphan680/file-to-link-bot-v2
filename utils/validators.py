"""Input validation utilities."""
import re
from typing import Optional, List
from utils.constants import USER_ID_PATTERN, CHANNEL_PATTERN, URL_PATTERN


def validate_user_id(user_id: any) -> bool:
    """Validate Telegram user ID."""
    try:
        uid = int(user_id)
        return 1000000 <= uid <= 9999999999
    except (ValueError, TypeError):
        return False


def validate_channel_id(channel_id: any) -> bool:
    """Validate Telegram channel ID."""
    try:
        cid = int(channel_id)
        return -9223372036854775808 <= cid <= -100000000000000
    except (ValueError, TypeError):
        return False


def validate_url(url: str) -> bool:
    """Validate URL format."""
    return bool(re.match(URL_PATTERN, url))


def validate_file_size(size: int, max_size: int = 2147483648) -> bool:
    """Validate file size."""
    return 0 < size <= max_size


def extract_user_ids(text: str) -> List[int]:
    """Extract user IDs from text."""
    pattern = r"\b\d{5,10}\b"
    matches = re.findall(pattern, text)
    user_ids = []
    for match in matches:
        if validate_user_id(match):
            user_ids.append(int(match))
    return list(set(user_ids))
