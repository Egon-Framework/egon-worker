"""The application command line interface"""

from argparse import ArgumentParser

from . import __version__


class Parser(ArgumentParser):
    """Defines the command line interface and handles command line argument parsing"""

    def __init__(self) -> None:
        """Define the command line interface"""

        super().__init__(prog='egon-worker', description='Worker process for launching jobs from the Egon load balancer.')
        self.add_argument('--version', action='version', version=__version__)
        subparsers = self.add_subparsers(parser_class=ArgumentParser, required=True)

        poll = subparsers.add_parser('poll')
        poll.set_defaults(action=Application.poll)
        poll.add_argument(
            '-v', action='count', dest='verbose', default=0,
            help='set output verbosity to warning (-v), info (-vv), or debug (-vvv)')


class Application:
    """Entry point for instantiating and executing the application"""

    @staticmethod
    def poll(*args, **kwargs) -> None:
        """Poll the load balancer for new jobs and launch them on the current machine"""

        raise NotImplementedError('Polling is not implemented yet')

    @classmethod
    def execute(cls) -> None:
        """Parse command line arguments and run the application"""

        parser = Parser()
        args = vars(parser.parse_args())
        action = args.pop('action')
        action(**args)
