import platform
import subprocess

from switchtest.exceptions import ValidationExecutionError


def ping_target(target: str, timeout: int = 30) -> tuple[bool, str]:
    if not target:
        raise ValidationExecutionError("Ping validation requires a target")
    is_windows = platform.system().lower() == "windows"
    command = ["ping", "-n" if is_windows else "-c", "1", target]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ValidationExecutionError("ping utility is not available") from exc
    except subprocess.TimeoutExpired as exc:
        raise ValidationExecutionError(f"Ping timed out after {timeout} seconds") from exc
    output = (completed.stdout or "") + (completed.stderr or "")
    return completed.returncode == 0, output.strip()
