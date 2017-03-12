import cStringIO
import pycurl
import json
from neobunch import neobunchify as bunchify
from neobunch import NeoBunch as Bunch
from requests_oauthlib import OAuth2Session

from truehome.utils import Enum
from truehome.vendors import BaseVendorBridge


class TadoBridge(BaseVendorBridge):
    REMOTE_PORT = 443
    REMOTE_HOST = 'my.tado.com'
    REMOTE_URI = 'https://{host}:{port}'.format(host=REMOTE_HOST, port=REMOTE_PORT)

    TOKEN_URI = REMOTE_URI + '/oauth/token'
    HANDSHAKE_REQUEST = REMOTE_URI + '/api/v2/me'
    REQUEST_TEMPLATE = REMOTE_URI + '/api/v2/homes/{home_id}/zones/{zone_id}/{request_type}'

    READ_REQUEST_PARAMS_MAP = {
    }

    FAN_SPEED = Enum('HIGH', 'MIDDLE', 'LOW')
    SWING_STATES = Enum('ON', 'OFF')
    MODES = Enum('HEAT', 'COOL')

    DEFAULT_SWING_STATE = SWING_STATES.ON
    DEFAULT_FAN_SPEED = FAN_SPEED.MIDDLE

    CHANGE_REQUEST_PARAMS_MAP = {
        # Fan speed and swing status must be specified along with termination parameters.
        'setting': {
            'type': 'AIR_CONDITIONING',
            'fanSpeed': DEFAULT_FAN_SPEED,
            'swing': DEFAULT_SWING_STATE,
            'power': 'ON',
        },
        'termination': {
            'type': 'MANUAL'
        }
    }

    def __init__(self, **kwargs):
        super(TadoBridge, self).__init__(self, **kwargs)
        self._home_id = self.get_homes()[0].id

    def _load_config(self):
        self._username = 'nutcrook@gmail.com'
        self._password = 'qwer1234'

    def data_manipulation(self, **kwargs):
        zone_id = kwargs.pop('zone_id')
        # If the temperature is a list, then the user has set something out of range.
        # Use the mode to select on of the range bounds.
        if isinstance(kwargs['temperature'], list):
            if kwargs['mode'] == self.MODES.HEAT:
                kwargs['temperature'] = dict(celsius=int(kwargs['temperature'][-1]))
            elif kwargs['mode'] == self.MODES.COOL:
                kwargs['temperature'] = dict(celsius=int(kwargs['temperature'][0]))
        else:
            kwargs['temperature'] = dict(celsius=int(kwargs['temperature']))

        self.CHANGE_REQUEST_PARAMS_MAP['setting'].update(kwargs)

        try:
            token = self._get_token(self._username, self._password)
            tado_session = OAuth2Session(client_id='tado-webapp', token=token)
            tado_session.headers['Content-Type'] = 'application/json;charset=UTF-8'
            r = tado_session.put(data=json.dump(self.CHANGE_REQUEST_PARAMS_MAP),
                                 url=self.REQUEST_TEMPLATE.format(request_type='overlay',
                                                                  home_id=self._home_id,
                                                                  zone_id=zone_id))
            if r.status_code == 200:
                return r.text
            else:
                return 'Whoops! Return Code {}: {}'.format(r.status_code, r.text)
        except Exception as e:
            return 'Oh Snap! An exception: {}'.format(str(e))

    def data_retrieval(self, **kwargs):
        kwargs.update(request_type='state', home_id=self._home_id)
        try:
            token = self._get_token(self._username, self._password)
            tado_session = OAuth2Session(client_id='tado-webapp', token=token)
            r = tado_session.get(self.REQUEST_TEMPLATE.format(kwargs))
            if r.status_code == 200:
                return r.text
            else:
                return 'Whoops! Return Code {}: {}'.format(r.status_code, r.text)
        except Exception as e:
            return str(e)

    def check_connectivity(self):
        raise NotImplementedError

    def _get_token(self, username, password):
        curl = pycurl.Curl()
        curl.setopt(curl.URL, self.TOKEN_URI)
        buffer = cStringIO.StringIO()
        curl.setopt(curl.WRITEFUNCTION, buffer.write)
        curl.setopt(curl.POSTFIELDS, ('client_id={client_id}&grant_type=password&password={password}&'
                                      'scope=home.user&username={username}').format(client_id='tado-webapp',
                                                                                    password=password,
                                                                                    username=username))
        curl.perform()
        response = json.loads(buffer.getvalue())
        return response

    def get_homes(self):
        try:
            token = self._get_token(self._username, self._password)
            tado_session = OAuth2Session(client_id='tado-webapp', token=token)
            r = tado_session.get(self.HANDSHAKE_REQUEST)
            if r.status_code == 200:
                return bunchify(json.loads(r.text)).homes
            else:
                return Bunch(error='Woops! Return Code {}: {}'.format(r.status_code, r.text))
        except Exception as e:
            return Bunch(error=str(e))
