from collections import deque
import time

from ..config import settings
from .signals import Opportunity


class RiskManager:
    def __init__(self):
        self.open_cycles = 0
        self.failure_timestamps = deque()

    def is_execution_allowed(self, opportunity: Opportunity) -> bool:
        """Check if an execution is allowed based on risk parameters."""
        if self.open_cycles >= settings.MAX_OPEN_CYCLES:
            return False

        # Circuit breaker logic
        now = time.time()
        while self.failure_timestamps and self.failure_timestamps[0] <= now - 60:
            self.failure_timestamps.popleft()
        if len(self.failure_timestamps) > 5: # e.g., 5 failures in the last minute
            return False

        if float(opportunity.max_qty_quote) > settings.MAX_LEG_NOTIONAL_QUOTE:
            return False

        return True

    def on_execution_start(self, opportunity: Opportunity):
        self.open_cycles += 1

    def on_execution_success(self, opportunity: Opportunity):
        self.open_cycles = max(0, self.open_cycles - 1)

    def on_execution_failure(self, opportunity: Opportunity):
        self.open_cycles = max(0, self.open_cycles - 1)
        self.failure_timestamps.append(time.time())
