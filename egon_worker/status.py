from enum import Enum


class Status(Enum):
    """Enumerated object representing node status values"""

    PENDING = 'pending'
    SETUP = 'setup'
    RUNNING = 'running'
    TEARDOWN = 'teardown'
    FINISHED = 'finished'
    DEGRADED = 'degraded'
    FAILED = 'failed'
