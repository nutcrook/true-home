from socket import socket
from neobunch import neobunchify as bunchify
from neobunch import NeoBunch as Bunch
import json
import requests

from truehome.vendors import BaseVendorBridge


class VeraBridge(BaseVendorBridge):
    REMOTE_PORT = 3480
    REMOTE_URI = BaseVendorBridge.REMOTE_URI.format(host=BaseVendorBridge.REMOTE_HOST,
                                                    port=REMOTE_PORT)
    REQUEST_TEMPLATE = REMOTE_URI + '/data_request'

    CHANGE_REQUEST_PARAMS_MAP = {
        # DeviceNum and newTargetValue are being populated later on.
        'id': 'action',
        'serviceId': 'urn:upnp-org:serviceId:SwitchPower1',
        'action': 'SetTarget',
        'output_format': 'json'
    }

    READ_REQUEST_PARAMS_MAP = {
        'data': {'id': 'sdata',
                 'output_format': 'json'}
    }

    def _fix_status(self, status):
        if isinstance(status, str):
            status = status.lower()

        if status in self.STATUS_MAP:
            return self.STATUS_MAP[status]
        else:
            raise KeyError('Invalid device state: {}'.format(status))

    def align_change_request_params(self, **request_params):
        request_params.update(self.CHANGE_REQUEST_PARAMS_MAP)

        request_params['DeviceNum'] = request_params['device_id']
        del request_params['device_id']

        request_params['newTargetValue'] = self._fix_status(request_params['status'])
        del request_params['status']

        return request_params

    def data_manipulation(self, **kwargs):
        def validate(**kwargs):
            device_id = kwargs.get('device_id')
            new_status = kwargs.get('status')

            data = bunchify(json.loads(self.data_retrieval(**kwargs)))
            device = [device for device in data.devices if device.id == device_id and int(device.status) != new_status]
            return device

        # Make sure the desired device (identified by device_id) has a status different form the desired status.
        if validate(**kwargs):
            request_params = self.align_change_request_params(**kwargs)
            try:
                r = requests.get(self.REQUEST_TEMPLATE, params=request_params)
                if r.status_code == 200:
                    return r.text
                else:
                    return 'Return Code {}: {}'.format(r.status_code, r.text)
            except Exception as e:
                return str(e)
        else:
            return 'Hi there, nothing to do. Sorry...'

    def data_retrieval(self, request_key='data', **kwargs):
        # Initialize request specific params
        request_params = self.READ_REQUEST_PARAMS_MAP[request_key]
        request_params.update(kwargs)

        try:
            r = requests.get(self.REQUEST_TEMPLATE, params=request_params)
            if r.status_code == 200:
                return r.text
            else:
                return 'Woops! Return Code {}: {}'.format(r.status_code, r.text)
        except Exception as e:
            return str(e)

    def check_connectivity(self):
        response = Bunch(connection_established=False)
        s = socket()
        try:
            s.connect((self.REMOTE_HOST, self.REMOTE_PORT))
            response.connection_established = True
        finally:
            return response
