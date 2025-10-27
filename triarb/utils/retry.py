from tenacity import retry, stop_after_attempt, wait_exponential

# Generic retry decorator for async functions
async_retry = retry(
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5),
)
