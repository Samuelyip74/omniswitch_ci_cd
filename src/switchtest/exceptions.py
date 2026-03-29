class SwitchTestError(Exception):
    """Base exception for the framework."""


class ConfigurationError(SwitchTestError):
    """Raised when runtime configuration is invalid."""


class ConnectionError(SwitchTestError):
    """Raised when a device connection fails."""


class AuthenticationError(ConnectionError):
    """Raised when authentication fails."""


class PromptDetectionError(ConnectionError):
    """Raised when the CLI prompt cannot be detected."""


class CommandExecutionError(SwitchTestError):
    """Raised when a device command fails."""


class ValidationExecutionError(SwitchTestError):
    """Raised when a validation cannot be executed."""


class CleanupError(SwitchTestError):
    """Raised when cleanup actions fail."""


class BaselineRestoreError(SwitchTestError):
    """Raised when baseline restoration fails."""


class LoaderError(SwitchTestError):
    """Raised when YAML loading or validation fails."""
