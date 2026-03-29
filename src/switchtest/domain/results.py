from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from switchtest.domain.enums import ResultStatus, SuiteStatus


class ValidationResult(BaseModel):
    name: str
    status: ResultStatus
    observed: Optional[str] = None
    expected: Optional[str] = None
    message: Optional[str] = None


class TestResult(BaseModel):
    test_id: str
    test_name: str
    status: ResultStatus
    started_at: datetime
    ended_at: datetime
    duration_seconds: float
    validation_results: list[ValidationResult] = Field(default_factory=list)
    command_log: list[str] = Field(default_factory=list)
    error_message: Optional[str] = None
    cleanup_status: Optional[str] = None


class SuiteResult(BaseModel):
    suite_name: str
    device_name: str
    platform: str
    firmware_version: Optional[str] = None
    device_model: Optional[str] = None
    started_at: datetime
    ended_at: datetime
    duration_seconds: float
    status: SuiteStatus
    tests: list[TestResult] = Field(default_factory=list)
