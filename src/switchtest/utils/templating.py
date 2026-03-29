from string import Template


def render_template(value: str, variables: dict[str, str]) -> str:
    return Template(value).safe_substitute(variables)
