"""The ``Settings`` module defines the application settings schema.

Application settings are defined as attributes of the ``Settings`` class,
including setting names, descriptions, and default values. The following
order of priority is used when resolving application settings:

  1. Commandline arguments provided at runtime
  2. Environment variables prefixed by the string ``EGON_``
  3. Default values defined by the ``Settings`` class
"""

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
