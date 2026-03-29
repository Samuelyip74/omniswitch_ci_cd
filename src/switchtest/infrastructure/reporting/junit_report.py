from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, SubElement

from switchtest.domain.enums import ResultStatus
from switchtest.domain.results import SuiteResult


def write_junit_report(path: Path, result: SuiteResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    testsuite = Element(
        "testsuite",
        name=result.suite_name,
        tests=str(len(result.tests)),
        failures=str(sum(1 for test in result.tests if test.status == ResultStatus.FAIL)),
        errors=str(sum(1 for test in result.tests if test.status == ResultStatus.ERROR)),
        skipped=str(sum(1 for test in result.tests if test.status == ResultStatus.SKIPPED)),
        time=f"{result.duration_seconds:.3f}",
    )
    for test in result.tests:
        case = SubElement(
            testsuite,
            "testcase",
            name=test.test_name,
            classname=result.suite_name,
            time=f"{test.duration_seconds:.3f}",
        )
        if test.status == ResultStatus.FAIL:
            failure = SubElement(case, "failure", message=test.error_message or "validation failure")
            failure.text = test.error_message or "One or more validations failed"
        elif test.status == ResultStatus.ERROR:
            error = SubElement(case, "error", message=test.error_message or "execution error")
            error.text = test.error_message or "Test execution error"
        elif test.status == ResultStatus.SKIPPED:
            SubElement(case, "skipped")
    ElementTree(testsuite).write(path, encoding="utf-8", xml_declaration=True)
