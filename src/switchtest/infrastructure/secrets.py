import os

from switchtest.exceptions import ConfigurationError


def get_required_secret(env_name: str) -> str:
    value = os.getenv(env_name)
    if not value:
        raise ConfigurationError(f"Required environment variable is missing: {env_name}")
    return value


def get_optional_secret(env_name: str | None) -> str | None:
    if not env_name:
        return None
    return os.getenv(env_name)
