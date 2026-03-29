from collections import Counter

from switchtest.domain.enums import ResultStatus
from switchtest.domain.results import SuiteResult


def render_suite_summary(result: SuiteResult) -> str:
    counts = Counter(test.status.value for test in result.tests)
    return (
        f"Suite: {result.suite_name}\n"
        f"Device: {result.device_name}\n"
        f"Platform: {result.platform}\n"
        f"Firmware: {result.firmware_version or 'unknown'}\n"
        f"Model: {result.device_model or 'unknown'}\n"
        f"Status: {result.status.value}\n"
        f"Pass: {counts.get(ResultStatus.PASS.value, 0)} "
        f"Fail: {counts.get(ResultStatus.FAIL.value, 0)} "
        f"Error: {counts.get(ResultStatus.ERROR.value, 0)} "
        f"Skipped: {counts.get(ResultStatus.SKIPPED.value, 0)}"
    )
