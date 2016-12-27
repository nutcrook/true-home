from functools import wraps
from truehome.utils.decorators import requires_authentication
import requests


REQUEST_TEMPLATE ='http://nutcrook.home.dyndns.org:3480/data_request'


CHANGE_REQUEST_PARAMS_MAP = {
    # DeviceNum and newTargetValue are being populated later on.
    'id': 'action',
    'serviceId': 'urn:upnp-org:serviceId:SwitchPower1',
    'action': 'SetTarget'
}

READ_REQUEST_PARAMS_MAP = {
    'data': {'id': 'sdata'}
}

BASE_PARAMS = {
    'output_format': 'json'
}


def align_change_request_params(**request_params):
    request_params.update(CHANGE_REQUEST_PARAMS_MAP)
    request_params.update(BASE_PARAMS)

    request_params['DeviceNum'] = request_params['device_id']
    del request_params['device_id']

    request_params['newTargetValue'] = request_params['status']
    del request_params['status']

    return request_params


def data_manipulation(**kwargs):
    request_params = align_change_request_params(**kwargs)
    try:
        r = requests.get(REQUEST_TEMPLATE, params=request_params)
        if r.status_code == 200:
            return r.text
        else:
            return 'Return Code {}: {}'.format(r.status_code, r.text)
    except Exception as e:
        return str(e)


def data_retrieval(request_key='data', **kwargs):
    # Initialize request specific params
    request_params = READ_REQUEST_PARAMS_MAP[request_key]
    request_params.update(kwargs)
    # Add the base parameters
    request_params.update(BASE_PARAMS)
    try:
        r = requests.get(REQUEST_TEMPLATE, params=request_params)
        if r.status_code == 200:
            return r.text
        else:
            return 'Return Code {}: {}'.format(r.status_code, r.text)
    except Exception as e:
        return str(e)


@requires_authentication()
def true_home_api(request_key='data', transparent=False):
    def api_decorator(func, **kwargs):
        @wraps(func)
        def wrapper(**kwargs):
            if transparent:
                return func(**kwargs)
            else:
                return data_retrieval(request_key, **kwargs)

        if transparent:
            setattr(wrapper, 'data', data_retrieval(request_key, **kwargs))
        setattr(wrapper, 'key', request_key)
        return wrapper

    return api_decorator
