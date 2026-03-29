from pathlib import Path

from switchtest.infrastructure.loaders.devices import load_devices
from switchtest.infrastructure.loaders.suites import load_suite_testcases
from switchtest.infrastructure.loaders.testcases import load_testcase


def test_load_devices() -> None:
    devices = load_devices(Path("configs/devices.yaml"))
    assert "ACSSW01" in devices
    assert devices["ACSSW01"].platform == "aos"


def test_load_testcase() -> None:
    testcase = load_testcase(Path("testcases/vlan/vlan_create.yaml"))
    assert testcase.id == "TC-VLAN-001"
    assert len(testcase.validations) == 2


def test_load_suite_testcases() -> None:
    suite, tests = load_suite_testcases(Path("suites/smoke.yaml"))
    assert suite.name == "smoke"
    assert len(tests) >= 1
