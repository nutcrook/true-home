from neobunch import neobunchify as bunchify
from flask import Flask, request
from relayer_requests import true_home_api, data_retrieval, data_manipulation
import json

app = Flask(__name__)


@app.route('/summary', methods=['GET'])
@true_home_api()
def get_all_data(**kwargs):
    pass


@app.route('/rooms/')
@app.route('/rooms/<int:room_id>')
@true_home_api(transparent=True)
def all_rooms(room_id=None, **kwargs):
    data = all_rooms.data
    if data:
        data = bunchify(json.loads(data))

    if room_id:
        room = [room for room in data.rooms if room.id == room_id]
        if len(room) == 1:
            data = json.dumps(room)

    return data


@app.route('/devices', methods=['GET'])
@app.route('/devices/<int:device_id>', methods=['GET'])
@true_home_api(transparent=True)
def get_devices(device_id=None, **kwargs):
    data = get_devices.data
    if data:
        data = bunchify(json.loads(data))

    if device_id:
        device = [device for device in data.devices if device.id == device_id]
        if len(device) == 1:
            data = json.dumps(device)

    return data


@app.route('/devices/by-room/<int:room_id>', methods=['GET'])
@true_home_api(transparent=True)
def get_devices_in_room(room_id=None, **kwargs):
    data = get_devices_in_room.data
    if data:
        data = bunchify(json.loads(data))

    if room_id:
        device = [device for device in data.devices if device.room == room_id]
        data = json.dumps(device)

    return data


@app.route('/devices/<int:device_id>/<int:status>', methods=['GET'])
@true_home_api(transparent=True)
def set_device_status(device_id, status):
    return data_manipulation(**{'device_id': device_id,
                                'status': status})

if __name__ == '__main__':
    app.run(debug=True)
