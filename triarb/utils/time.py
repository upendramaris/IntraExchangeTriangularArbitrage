import time


def now_ms() -> int:
    """Current time in milliseconds."""
    return int(time.time() * 1000)
