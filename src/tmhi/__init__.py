import time

from requisitor.session import Session

from .dataclasses.ap import AP
from .dataclasses.gateway import Gateway
from .dataclasses.telemetry import Telemetry

API_BASE = 'http://192.168.12.1:8080/TMI/v1'


class TMHI:
    def __init__(self, username='admin', password='admin'):
        self.username = username
        self.password = password

        self._token = None
        self._token_exp = None

        self._session = Session()

    def _get(self, *args, **kwargs):
        self._session.headers['Authorization'] = f'Bearer {self.token}'
        return self._session.get(*args, **kwargs)

    def _post(self, *args, **kwargs):
        self._session.headers['Authorization'] = f'Bearer {self.token}'
        return self._session.post(*args, **kwargs)

    @property
    def token(self):
        if self._token_exp and time.time() > self._token_exp:
            self.refresh()

        return self._token

    def login(self):
        url = f'{API_BASE}/auth/login'
        r = self._post(
            url,
            json={
                'username': self.username,
                'password': self.password,
            },
        )
        data = r.json()
        self._token = data['auth']['token']
        self._token_exp = data['auth']['expiration']

    def refresh(self):
        url = f'{API_BASE}/auth/refresh'
        self._post(url)

    def version(self):
        url = f'{API_BASE}/version'
        return self._get(url).json()['version']

    def get_ap_configuration(self):
        url = f'{API_BASE}/network/configuration/v2'
        data = self._get(url, params={'get': 'ap'}).json()
        return AP(**data)

    def set_ap_configuration(self, ap):
        url = f'{API_BASE}/network/configuration/v2'
        data = ap.asdict()
        self._post(url, params={'set': 'ap'}, json=data)

    def telemetry(self):
        url = f'{API_BASE}/network/telemetry'
        data = self._get(url, params={'get': 'all'}).json()
        return Telemetry(**data)

    def clients(self):
        return self.telemetry().clients

    def gateway_info(self, device=True, signal=False, time=True):
        url = f'{API_BASE}/gateway'
        data = self._get(url, params={'get': 'all'}).json()
        return Gateway(**data)

    def change_password(self, password):
        url = f'{API_BASE}/auth/admin/reset'
        self._post(
            url,
            json={
                'usernameNew': self.username,
                'passwordNew': password,
            },
        )
        self.password = password
        self.login()

    def reboot(self):
        url = f'{API_BASE}/gateway/reset?set=reboot'
        self._post(url)
