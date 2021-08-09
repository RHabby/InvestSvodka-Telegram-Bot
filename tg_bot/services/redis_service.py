from typing import List, Optional

import redis

r = redis.Redis(host="localhost", port=6379, db=0)


def set_value(key: str, value: str) -> None:
    """Set simple key-value"""
    r.set(key, value)


def get_value(key: str) -> Optional[bytes]:
    """Get simple key-value"""
    return r.get(key)


def get_list(key: str) -> List[bytes]:
    """Get full list"""
    return r.lrange(name=key, start=0, end=-1)
