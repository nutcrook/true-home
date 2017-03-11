from werkzeug.routing import BaseConverter
from truehome.vendors import AC_TEMPERATURE_RANGE


class StatusConverter(BaseConverter):
    def to_python(self, value):
        return value

    def to_url(self, value):
        return BaseConverter.to_url(value)


class TadoTemperatureConverter(BaseConverter):
    def to_python(self, value):
        if int(value) not in AC_TEMPERATURE_RANGE:
            return [AC_TEMPERATURE_RANGE[0], AC_TEMPERATURE_RANGE[-1]]
        return value

    def to_url(self, value):
        return value


class TadoModeConverter(BaseConverter):
    def to_python(self, value):
        return value.upper()

    def to_url(self, value):
        return value.lower()


class Enum(object):
    def __init__(self, *args):
        self._internal_dict = dict()
        for arg in args:
            self._internal_dict[arg] = arg

    def __dir__(self):
        return self._internal_dict.keys()

    def __getattr__(self, item):
        if item in self._internal_dict:
            return self._internal_dict[item]
        else:
            return KeyError('{} not part of the enum'.format(item))

VENDORS = Enum('Vera', 'Tado')
