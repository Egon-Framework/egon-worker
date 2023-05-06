"""The ``Settings`` defines the application's settings schema, including setting
names, descriptions, and default values.
"""


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
