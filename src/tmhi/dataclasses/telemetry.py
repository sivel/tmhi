from dataclasses import dataclass
from dataclasses import field
from ipaddress import IPv4Address
from ipaddress import IPv6Address

from .base import TMHIDataClass


@dataclass(init=False, kw_only=True)
class SIM(TMHIDataClass):
    iccId: str
    imei: str
    imsi: str
    msisdn: str
    status: bool


@dataclass(init=False, kw_only=True)
class Neighbor(TMHIDataClass):
    bands: list[str]
    bars: float
    cid: int
    gNBID: float
    rsrp: int
    rsrq: int
    rssi: int
    sinr: int


@dataclass(init=False, kw_only=True)
class Client(TMHIDataClass):
    connected: bool
    ipv4: IPv4Address
    ipv6: list[IPv6Address]
    mac: str
    name: str


@dataclass(init=False, kw_only=True)
class Clients(TMHIDataClass):
    band2_4ghz: list[Client] = field(metadata={'name': '2.4ghz'})
    band5_0ghz: list[Client] = field(metadata={'name': '5.0ghz'})
    ethernet: list[Client]


@dataclass(init=False, kw_only=True)
class CellSector(TMHIDataClass):
    bands: list[str]
    bars: float
    cid: int
    rsrp: int
    rsrq: int
    rssi: int
    sinr: int
    eNBID: int = field(default=None)  # 4g
    gNBID: int = field(default=None)  # 5g


@dataclass(init=False, kw_only=True)
class CellBand(TMHIDataClass):
    bandwidth: str
    cqi: int
    earfcn: str
    ecgi: str
    mcc: str
    mnc: str
    pci: str
    plmn: str
    sector: CellSector
    status: bool
    supportedBands: list[str]
    tac: str


@dataclass(init=False, kw_only=True)
class CellGeneric(TMHIDataClass):
    apn: str
    hasIPv6: bool
    registration: str
    roaming: bool


@dataclass(init=False, kw_only=True)
class CellGPS(TMHIDataClass):
    latitude: float
    longitude: float


@dataclass(init=False, kw_only=True)
class Cell(TMHIDataClass):
    band4g: CellBand = field(metadata={'name': '4g'})
    band5g: CellBand = field(metadata={'name': '5g'})
    generic: CellGeneric
    gps: CellGPS


@dataclass(init=False, kw_only=True)
class ACS(TMHIDataClass):
    checkin: int


@dataclass(init=False, kw_only=True)
class Telemetry(TMHIDataClass):
    acs: ACS
    cell: Cell
    clients: Clients
    neighbors: list[Neighbor]
    sim: SIM
