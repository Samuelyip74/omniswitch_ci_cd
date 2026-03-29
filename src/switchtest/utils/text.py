import re


def normalize_cli_output(text: str) -> str:
    return text.replace("\r\n", "\n").strip()


def redact_sensitive(text: str, secrets: list[str]) -> str:
    redacted = text
    for secret in secrets:
        if secret:
            redacted = redacted.replace(secret, "***")
    return redacted


def strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)
