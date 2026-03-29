from switchtest.drivers.aos import _extract_firmware, _extract_model


SHOW_SYSTEM_OUTPUT = """ACSW01-> show system

  Description:  Alcatel-Lucent Enterprise OS6860E-P24 8.9.221.R03 GA, October 12, 2023.,
  Object ID:    1.3.6.1.4.1.6486.801.1.1.2.1.11.1.6,
  Up Time:      12 days 4 hours 24 minutes and 21 seconds,
  Contact:      jerry.poh@al-enterprise.com,
  Name:         ACSW01,
  Location:     ALE Demo Lab,
  Services:     78,
  Date & Time:  SUN MAR 29 2026 15:43:07 (ZP8)
"""


def test_extract_model_from_show_system() -> None:
    assert _extract_model(SHOW_SYSTEM_OUTPUT) == "OS6860E-P24"


def test_extract_firmware_from_show_system() -> None:
    assert _extract_firmware(SHOW_SYSTEM_OUTPUT) == "8.9.221.R03 GA"
