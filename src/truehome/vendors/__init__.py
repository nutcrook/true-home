from truehome.utils import NotImplementedField


class BaseVendorBridge(object):
    REMOTE_PORT = NotImplementedField
    REMOTE_HOST = 'nutcrook.home.dyndns.org'
    REMOTE_URI = 'http://{host}:{port}'

    REQUEST_TEMPLATE = NotImplementedField

    CHANGE_REQUEST_PARAMS_MAP = NotImplementedField
    READ_REQUEST_PARAMS_MAP = NotImplementedField

    def align_change_request_params(self, **request_params):
        raise NotImplementedError

    def data_manipulation(self, **kwargs):
        raise NotImplementedError

    def data_retrieval(self, **kwargs):
        raise NotImplementedError

    def check_connectivity(self):
        raise NotImplementedError
