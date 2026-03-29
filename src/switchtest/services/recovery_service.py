from switchtest.drivers.base import BaseSwitchDriver


class RecoveryService:
    def reconnect(self, driver: BaseSwitchDriver) -> None:
        driver.disconnect()
        driver.connect()
