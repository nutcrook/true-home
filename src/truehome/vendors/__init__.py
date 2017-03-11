from truehome import NotImplementedField


AC_TEMPERATURE_RANGE = range(16, 31)


class BaseVendorBridge(object):
    REMOTE_PORT = NotImplementedField
    REMOTE_HOST = 'nutcrook.home.dyndns.org'
    REMOTE_URI = 'http://{host}:{port}'

    REQUEST_TEMPLATE = NotImplementedField

    CHANGE_REQUEST_PARAMS_MAP = NotImplementedField
    READ_REQUEST_PARAMS_MAP = NotImplementedField

    STATUS_MAP = {
        'on': 1,
        'off': 0,
        'enable': 1,
        'disable': 0,
        'true': int(True),
        'false': int(False),
        1: 1,
        0: 0
    }

    def __init__(self, read_config=False):
        if read_config:
            self._load_config()

    def _load_config(self):
        pass

    def align_change_request_params(self, **request_params):
        raise NotImplementedError

    def data_manipulation(self, **kwargs):
        raise NotImplementedError

    def data_retrieval(self, **kwargs):
        raise NotImplementedError

    def check_connectivity(self):
        raise NotImplementedError
