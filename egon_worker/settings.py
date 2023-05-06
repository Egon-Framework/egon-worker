"""The ``Settings`` module defines the application settings schema.

Application settings are defined as attributes of the ``Settings`` class,
including setting names, descriptions, and default values. The following
order of priority is used when resolving application settings:

  1. Commandline arguments provided at runtime
  2. Environment variables prefixed by the string ``EGON_``
  3. Default values defined by the ``Settings`` class
"""

from pathlib import Path
from typing import Literal

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Defines the application settings schema (setting names, default values, etc.)"""

    class Config:
        """Configure parsing options for application settings"""

        env_prefix = "EGON_"
        case_sensitive = False
        allow_mutation = False

    status_api_host: str = Field(title='API Server Host', default=None, description='Status API server host address')
    status_api_port: int = Field(title='API Server Port', default=5000, description='Status API server port number')

    # Logging settings
    log_path: Path = Field(title='Log Path', default=Path('/var/log/egon_worker.log'), description='Log file path')
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(
        title='Logging Level', default='INFO', description='Logging threshold for recording to the log file')

    def get_logging_config(self) -> dict:
        """Return a dictionary with configuration settings for the Python logger"""

        return {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'default': {
                    'format': '%(asctime)s [%(process)d] %(levelname)8s %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                    'formatter': 'default',
                    'level': 0
                },
                'log_file': {
                    'class': 'logging.handlers.FileHandler',
                    'formatter': 'default',
                    'level': self.log_level,
                    'filename': self.log_path,
                }
            },
            'loggers': {
                'root': {'handlers': ['console', 'log_file'], 'level': 'INFO', 'propagate': False}
            }
        }
