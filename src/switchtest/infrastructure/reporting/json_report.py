from pathlib import Path

from switchtest.domain.results import SuiteResult


def write_json_report(path: Path, result: SuiteResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
