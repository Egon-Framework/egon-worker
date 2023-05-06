"""The ``status`` module provides a programmatic interface for the Egon Status API.

The ``RemoteStatusReporter`` class is used to report/fetch Egon job status
to/from  the Egon Status API. If running locally, or in an environment where
the status API is not available, the ``LocalStatusReporter`` class acts as a
drop in replacement.
"""

import abc
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


class AbstractStatusReporter(metaclass=abc.ABCMeta):
    """Abstract cass for defining the interface of status reporting objects"""

    @abc.abstractmethod
    def report_status(self, egn_id: str, status: Status, message: str | None = '') -> None:
        """Report the status of a Node object to the Status API"""


class LocalStatusReporter(AbstractStatusReporter):
    """Status reporting object used when running on a single system

    For running on distributed systems, see the ``RemoteStatusReporter`` class.
    """

    def report_status(self, egn_id: str, status: Status, message: str | None = '') -> None:
        """Report the status of a Node object to the Status API"""

        raise NotImplementedError()


class RemoteStatusReporter(AbstractStatusReporter):
    """Status reporting object used when running on distributed systems

    For running on non-distributed systems, see the ``LocalStatusReporter`` class.
    """

    def report_status(self, egn_id: str, status: Status, message: str | None = '') -> None:
        """Report the status of a Node object to the Status API"""

        raise NotImplementedError()


class StatusReporter:
    """Factory class for creating reporting objects based on application settings

    The returned instance type is determined automatically based on current
    application settings.
    """

    def __new__(cls) -> LocalStatusReporter | RemoteStatusReporter:
        """Return a new status reporter instance"""

        raise NotImplementedError('Local status reporting is not implemented yet')
