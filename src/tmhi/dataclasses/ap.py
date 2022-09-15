from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field

from .base import TMHIDataClass


def _convert_transmission_power(v):
    return int(f'{v}'.replace('%', ''))


@dataclass(init=False, kw_only=True)
class FrequencyBand(TMHIDataClass):
    airtimeFairness: bool = field(default=True)
    channel: str = field(default='Auto')
    channelBandwidth: str = field(default='Auto')
    isMUMIMOEnabled: bool = field(default=True)
    isRadioEnabled: bool = field(default=True)
    isWMMEnabled: bool = field(default=True)
    maxClients: int = field(default=128)
    mode: str = field(default='auto')
    transmissionPower: int = field(
        default=100,
        metadata={'converter': _convert_transmission_power},
    )

    def asdict(self):
        d = asdict(self)
        d['transmissionPower'] = f'{self.transmissionPower}%'
        return d


@dataclass(init=False, kw_only=True)
class FrequencyBands(TMHIDataClass):
    ghz2_4: FrequencyBand
    ghz5_0: FrequencyBand

    def asdict(self):
        d = asdict(self)
        d['2.4ghz'] = d.pop('ghz2_4').asdict()
        d['5.0ghz'] = d.pop('ghz5_0').asdict()
        return d


@dataclass(init=False, kw_only=True)
class SSID(TMHIDataClass):
    Ssid2_4ghz: bool = field(default=True, metadata={'name': '2.4ghzSsid'})
    Ssid5_0ghz: bool = field(default=True, metadata={'name': '5.0ghzSsid'})
    encryptionMode: str = field(default='AES')
    encryptionVersion: str = field(default='WPA2/WPA3')
    guest: bool = field(default=False)
    isBroadcastEnabled: bool = field(default=True)
    ssidName: str = field(default=None)
    wpaKey: str = field(default=None)

    def __post_init__(self):
        super().__post_init__()
        if self.ssidName is None:
            raise TypeError('ssidName is required')
        if self.wpaKey is None:
            raise TypeError('wpaKey is required')

    def asdict(self):
        d = asdict(self)
        d['2.4ghzSsid'] = d.pop('Ssid2_4ghz')
        d['5.0ghzSsid'] = d.pop('Ssid5_0ghz')
        return d


@dataclass(init=False, kw_only=True)
class SSIDs(TMHIDataClass):
    ssids: list[SSID]

    def asdict(self):
        return {'ssids': [s.asdict() for s in self.ssids]}


@dataclass(init=False, kw_only=True)
class BandSteering(TMHIDataClass):
    isEnabled: bool = field(default=False)

    def asdict(self):
        return asdict(self)


@dataclass(init=False, kw_only=True)
class AP(TMHIDataClass):
    ghz2_4: FrequencyBand = field(metadata={'name': '2.4ghz'})
    ghz5_0: FrequencyBand = field(metadata={'name': '5.0ghz'})
    ssids: list[SSID]
    bandSteering: BandSteering

    def asdict(self):
        d = {
            '2.4ghz': self.ghz2_4.asdict(),
            '5.0ghz': self.ghz5_0.asdict(),
            'ssids': [s.asdict() for s in self.ssids],
            'bandSteering': self.bandSteering.asdict(),
        }

        return d
