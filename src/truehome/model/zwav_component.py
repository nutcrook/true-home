class ZWaveComponent(object):
    def __init__(self, z_id, name, room_id, room_name, switchable=True):
        self._z_id = z_id
        self._name = name
        self._room_id = room_id
        self._room_name = room_name
        self._switchable = switchable
