import re


PROMPT_PATTERN = re.compile(r"(?m)[^\n\r]+[>#]\s?$")


def detect_prompt(text: str) -> str | None:
    match = PROMPT_PATTERN.search(text)
    if not match:
        return None
    return match.group(0).strip()
