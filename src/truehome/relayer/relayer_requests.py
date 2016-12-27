from neobunch import neobunchify as bunchify
from functools import wraps
import json
import requests


REQUEST_TEMPLATE ='http://nutcrook.home.dyndns.org:3480/data_request'


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


def null_func(**kwargs):
    return '{}'


def align_change_request_params(**request_params):
    request_params.update(CHANGE_REQUEST_PARAMS_MAP)

    request_params['DeviceNum'] = request_params['device_id']
    del request_params['device_id']

    request_params['newTargetValue'] = request_params['status']
    del request_params['status']

    return request_params


def data_manipulation(**kwargs):
    def validate(**kwargs):
        device_id = kwargs.get('device_id')
        new_status = kwargs.get('status')

        data = bunchify(json.loads(data_retrieval(**kwargs)))
        device = [device for device in data.devices if device.id == device_id and int(device.status) != new_status]
        return device

    # Make sure the desired device (identified by device_id) has a status different form the desired status.
    if validate(**kwargs):
        request_params = align_change_request_params(**kwargs)
        try:
            r = requests.get(REQUEST_TEMPLATE, params=request_params)
            if r.status_code == 200:
                return r.text
            else:
                return 'Return Code {}: {}'.format(r.status_code, r.text)
        except Exception as e:
            return str(e)
    else:
        return 'Hi there, nothing to do. Sorry...'


def data_retrieval(request_key='data', **kwargs):
    # Initialize request specific params
    request_params = READ_REQUEST_PARAMS_MAP[request_key]
    request_params.update(kwargs)

    try:
        r = requests.get(REQUEST_TEMPLATE, params=request_params)
        if r.status_code == 200:
            return r.text
        else:
            return 'Woops! Return Code {}: {}'.format(r.status_code, r.text)
    except Exception as e:
        return str(e)


def true_home_api(permission_needed):
    def api_decorator(func, **kwargs):
        @wraps(func)
        def wrapper(**kwargs):
            if permission_needed or not permission_needed:
                # Can the user perform the action?
                # Validation goes here.
                return func(**kwargs)

        return wrapper
    return api_decorator
