from pathlib import Path

from switchtest.app import RunArguments, run_application
from switchtest.exitcodes import ExitCode


def test_run_application_invalid_input_returns_invalid_input_code() -> None:
    exit_code = run_application(
        RunArguments(
            device_name="missing",
            suite_path=Path("suites/smoke.yaml"),
            devices_file=Path("configs/devices.yaml"),
            report_dir=Path("reports"),
            dry_run=True,
        )
    )
    assert exit_code == int(ExitCode.INVALID_INPUT)


def test_run_application_dry_run_returns_success() -> None:
    exit_code = run_application(
        RunArguments(
            device_name="ACSSW01",
            suite_path=Path("suites/smoke.yaml"),
            devices_file=Path("configs/devices.yaml"),
            report_dir=Path("reports"),
            dry_run=True,
        )
    )
    assert exit_code == int(ExitCode.SUCCESS)
