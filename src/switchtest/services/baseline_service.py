from switchtest.domain.device import DeviceDefinition
from switchtest.domain.enums import DeviceSafetyState
from switchtest.domain.runtime import RuntimeContext
from switchtest.drivers.base import BaseSwitchDriver
from switchtest.exceptions import BaselineRestoreError


class BaselineService:
    def verify_baseline(self, driver: BaseSwitchDriver, device: DeviceDefinition) -> None:
        if device.expected_prompt:
            driver.run_show("", timeout=device.command_timeout)

    def restore(self, context: RuntimeContext, driver: BaseSwitchDriver, device: DeviceDefinition) -> None:
        try:
            driver.restore_baseline(device.baseline_source)
            context.device_state = DeviceSafetyState.SAFE
        except Exception as exc:
            context.device_state = DeviceSafetyState.UNSAFE
            raise BaselineRestoreError(str(exc)) from exc
