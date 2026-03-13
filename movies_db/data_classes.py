from dataclasses import dataclass
from datetime import datetime


@dataclass
class RealFile:
    """Store a file data."""

    name: str
    path: str
    size: int
    last_mod: datetime
    hash_: str


@dataclass
class Device:
    """Store a device data."""

    capacity: int = 0
    free: int = 0
    st_dev: str = ""


@dataclass
class DeviceFiles:
    """Store list of files and the device object."""

    device: Device
    files: list[RealFile]
