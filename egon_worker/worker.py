import functools
import multiprocessing as mp

from egon import Node

from egon_worker.status import Status


class Worker:
    """Worker objects poll the load balancer for new jobs and launch them on the current machine."""

    @staticmethod
    def update_status(egon_id: str, status: Status, message: str = '') -> None:
        """Post a status update to the status API server

        Args:
            egon_id: UUID used to identify the running node
            status: The status of the running node
            message: Optional message detailing the reason for the status
        """

        # TODO: Reporting logic not implemented yet

    @classmethod
    def wrap_action(cls, egon_id: str, action: callable) -> callable:
        """Wrap a callable object with an error callback to the status API

        Args:
            egon_id: UUID used to identify the running node  
            action: The callable action to wrap

        Returns:
            A wrapper function around the given callable
        """

        # noinspection PyBroadException
        @functools.wraps(action)
        def wrapped() -> None:
            """Execute the wrapped callable and update the status API if an exception is raised"""

            try:
                action()

            except Exception:
                cls.update_status(egon_id, Status.DEGRADED)

        return wrapped

    @classmethod
    def wrap_node(cls, egon_id, node_class: type[Node], num_processes: int, args: tuple, kwargs: dict) -> callable:
        """Wrap a ``Node`` object with update calls to the status API

        Args:
            egon_id: UUID used to identify the running node
            node_class: The node class to execute
            num_processes: The number of processes to allocate the running node
            args: Tuple of arguments used to instantiate the node
            kwargs: Dictionary of keyword arguments used to instantiate the node

        Returns:
            A wrapper function for executing the given node
        """

        # noinspection PyBroadException
        def wrapped():
            try:
                # Create a new node instance and wrap the ``action`` method with callbacks to the status api
                node = node_class(*args, **kwargs)
                wrapped_action = cls.wrap_action(egon_id, node.action)
                processes = [mp.Process(target=wrapped_action) for _ in range(num_processes)]

                cls.update_status(egon_id, Status.RUNNING)
                node.class_setup()

                cls.update_status(egon_id, Status.RUNNING)
                for proc in processes:
                    proc.start()

                for proc in processes:
                    proc.join()

                cls.update_status(egon_id, Status.TEARDOWN)
                node.teardown()

            except Exception:
                cls.update_status(egon_id, Status.FAILED)

            else:
                cls.update_status(egon_id, Status.FINISHED)

        return wrapped

    def run_node(self, egon_id: str, node_class: type[Node], num_processes: int, args: tuple, kwargs: dict) -> None:
        """Launch a node object on the local machine using the given configuration arguments

        Args:
            egon_id: UUID used to identify the running node
            node_class: The node class to execute
            num_processes: The number of processes to allocate the running node
            args: Tuple of arguments used to instantiate the node
            kwargs: Dictionary of keyword arguments used to instantiate the node
        """

        executable = self.wrap_node(egon_id, node_class, num_processes, args, kwargs)
        process = mp.Process(target=executable)
        process.start()

    def poll(self) -> None:
        """Poll the load balancer and launch new nodes in real time"""

        raise NotImplementedError('Polling from the load balancer is not implimented yet')
