"""The ``status`` provides reporter class objects for interacting with the
Egon status server.
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
    """Factory class returning the appropriate reporting object based on application settings"""

    def __new__(cls, remote: bool) -> AbstractStatusReporter:
        """Return a new status reporter instance"""

        if remote:
            raise NotImplementedError('Remote status reporting is not implemented yet')

        raise NotImplementedError('Local status reporting is not implemented yet')
