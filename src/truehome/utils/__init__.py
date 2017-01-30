@property
def NotImplementedField(self):
    raise NotImplementedError('Property not implemented for {}'.format(self))


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

VENDORS = Enum('Vera')