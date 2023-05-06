"""The ``cli`` module defines the application's command line interface."""

import logging
import sys
from argparse import ArgumentParser

from . import __version__


class BaseParser(ArgumentParser):
    """Base class for creating argument parsers

    This class extends/overrides the built-in ``ArgumentParser`` to provide
    better error handling, help text formatting, etc..

    Encapsulating these changes as a dedicated class (instead of directly
    overriding methods in the default application ``Parser`` class) allows
    subparsers to share the same behavior as their parent parser
    (e.g., ``parent_parser.add_subparsers(parser_class=BaseParser)``).
    """

    def error(self, message: str) -> None:
        """Exit the parser by raising a ``SystemExit`` error

        If the parser was called without any commandline arguments, the parser
        help text is printed before exiting.

        Args:
            message: The error message

        Raises:
            SystemExit: Every time the method is run
        """

        if len(sys.argv) <= 1:
            self.print_help()

        raise SystemExit(f'Error: {message}')


class Parser(BaseParser):
    """Defines the command line interface and handles command line argument parsing"""

    def __init__(self) -> None:
        """Define the command line interface"""

        super().__init__(prog='egon-worker', description='Worker process for launching jobs from the Egon load balancer.')
        self.add_argument('--version', action='version', version=__version__)
        subparsers = self.add_subparsers(parser_class=BaseParser, required=True)

        poll = subparsers.add_parser('poll')
        poll.set_defaults(action=Application.poll)
        poll.add_argument(
            '-v', action='count', dest='verbose', default=0,
            help='set output verbosity to warning (-v), info (-vv), or debug (-vvv)')


class Application:
    """Entry point for instantiating and executing the application from the command line"""

    @staticmethod
    def poll(*args, **kwargs) -> None:
        """Poll the load balancer for new jobs and launch them on the current machine"""

        raise NotImplementedError('Polling is not implemented yet.')

    @classmethod
    def execute(cls) -> None:
        """Parse command line arguments and run the application"""

        parser = Parser()
        args = vars(parser.parse_args())
        action = args.pop('action')

        try:
            action(**args)

        except Exception as excep:
            logging.critical(str(excep))
