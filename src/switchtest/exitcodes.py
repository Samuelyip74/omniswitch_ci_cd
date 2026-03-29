from enum import IntEnum


class ExitCode(IntEnum):
    SUCCESS = 0
    TEST_FAILURE = 1
    FRAMEWORK_ERROR = 2
    DEVICE_CONNECTION_ERROR = 3
    CLEANUP_FAILURE = 4
    INVALID_INPUT = 5
