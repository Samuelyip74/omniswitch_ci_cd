from switchtest.drivers.aos import _clean_show_output


def test_clean_show_output_removes_prompt_echo() -> None:
    raw = """ACSW01-> show system

  Description:  Alcatel-Lucent Enterprise OS6860E-P24 8.9.221.R03 GA, October 12, 2023.,
  Object ID:    1.3.6.1.4.1.6486.801.1.1.2.1.11.1.6,
"""
    cleaned = _clean_show_output(raw, "show system")
    assert "ACSW01-> show system" not in cleaned
    assert "Description:" in cleaned


def test_clean_show_output_preserves_empty_when_only_echo() -> None:
    raw = "ACSW01-> show system\n"
    assert _clean_show_output(raw, "show system") == ""
