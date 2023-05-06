"""The ``Settings`` defines the application's settings schema, including setting
names, descriptions, and default values.
"""

from pathlib import Path
from typing import Literal

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Defines the application settings schema (setting names, default values, etc.)"""

    class Config:
        """Configure settings parsing options"""

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
