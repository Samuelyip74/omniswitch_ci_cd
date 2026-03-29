from pathlib import Path
from typing import Any

import yaml

from switchtest.exceptions import LoaderError


def load_yaml_file(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}
    except FileNotFoundError as exc:
        raise LoaderError(f"YAML file not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise LoaderError(f"Invalid YAML in {path}: {exc}") from exc


def resolve_relative_path(base_file: Path, target: str) -> Path:
    path = Path(target)
    if path.is_absolute():
        return path
    return (base_file.parent / path).resolve()
