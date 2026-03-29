from pydantic import BaseModel, Field


class SuiteDefinition(BaseModel):
    name: str
    description: str = ""
    tests: list[str] = Field(default_factory=list)
