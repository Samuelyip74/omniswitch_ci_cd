from switchtest.drivers.base import BaseSwitchDriver


class MetadataService:
    def collect(self, driver: BaseSwitchDriver) -> dict[str, str | None]:
        return driver.get_metadata()
