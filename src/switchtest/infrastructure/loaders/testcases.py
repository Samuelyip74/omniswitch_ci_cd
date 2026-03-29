from pathlib import Path

from switchtest.domain.testcase import TestCaseDefinition
from switchtest.exceptions import LoaderError
from switchtest.infrastructure.loaders.common import load_yaml_file


def load_testcase(path: Path) -> TestCaseDefinition:
    payload = load_yaml_file(path)
    try:
        return TestCaseDefinition.model_validate(payload)
    except Exception as exc:
        raise LoaderError(f"Invalid testcase file {path}: {exc}") from exc
