from pathlib import Path

from switchtest.domain.device import DeviceDefinition, DeviceInventory
from switchtest.exceptions import LoaderError
from switchtest.infrastructure.loaders.common import load_yaml_file


def load_devices(path: Path) -> dict[str, DeviceDefinition]:
    payload = load_yaml_file(path)
    try:
        inventory = DeviceInventory.model_validate(payload)
    except Exception as exc:
        raise LoaderError(f"Invalid devices file {path}: {exc}") from exc
    return {device.name: device for device in inventory.devices}


def load_device_by_name(path: Path, device_name: str) -> DeviceDefinition:
    devices = load_devices(path)
    try:
        return devices[device_name]
    except KeyError as exc:
        raise LoaderError(f"Unknown device '{device_name}' in {path}") from exc
