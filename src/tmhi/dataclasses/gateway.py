from dataclasses import dataclass
from dataclasses import field

from packaging.version import Version

from .base import TMHIDataClass
from .telemetry import CellGeneric
from .telemetry import CellSector


@dataclass(init=False, kw_only=True)
class Device(TMHIDataClass):
    friendlyName: str
    hardwareVersion: str
    isEnabled: bool
    isMeshSupported: bool
    macId: str
    manufacturer: str
    manufacturerOUI: str
    model: str
    name: str
    role: str
    serial: str
    softwareVersion: Version
    type: str
    updateState: str


@dataclass(init=False, kw_only=True)
class Signal(TMHIDataClass):
    band4g: CellSector = field(metadata={'name': '4g'})
    band5g: CellSector = field(metadata={'name': '5g'})
    generic: CellGeneric


@dataclass(init=False, kw_only=True)
class DaylightSavings(TMHIDataClass):
    isUsed: bool


@dataclass(init=False, kw_only=True)
class Time(TMHIDataClass):
    daylightSavings: DaylightSavings
    localTime: int
    localTimeZone: str
    upTime: int


@dataclass(init=False, kw_only=True)
class Gateway(TMHIDataClass):
    device: Device
    signal: Signal
    time: Time
