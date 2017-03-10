from neobunch import neobunchify as bunchify
from flask import Flask, jsonify
from relayer_requests import true_home_api
import json

from truehome.utils import VENDORS
from truehome.utils import StatusConverter
from truehome.utils.scheduling.schedule_api import get_scheduled_jobs, delete_at_job, delete_cron_job
from truehome.vendors.vera.api import VeraBridge

app = Flask(__name__)
app.url_map.converters['status'] = StatusConverter

VENDORS_API = {
    VENDORS.Vera: VeraBridge()
}


def prepare_response(data):
    response = jsonify(data)
    return response


@app.route('/summary', methods=['GET'])
@true_home_api(permission_needed=True)
def get_all_data(**kwargs):
    data = VENDORS_API[VENDORS.Vera].data_retrieval(**kwargs)
    return data


@app.route('/rooms', methods=['GET'])
@app.route('/rooms/<int:room_id>')
@true_home_api(permission_needed=False)
def all_rooms(room_id=None, **kwargs):
    if room_id:
        kwargs.update({'room_id': room_id})
    data = VENDORS_API[VENDORS.Vera].data_retrieval(**kwargs)
    if data:
        data = bunchify(json.loads(data))

    if room_id:
        room = [room for room in data.rooms if room.id == room_id]
        if len(room) == 1:
            data = room
    else:
        data = data.rooms

    return prepare_response(data)


@app.route('/devices', methods=['GET'])
@app.route('/devices/<int:device_id>', methods=['GET'])
@true_home_api(permission_needed=False)
def get_devices(device_id=None, **kwargs):
    if device_id:
        kwargs.update({'device_id': device_id})
    data = VENDORS_API[VENDORS.Vera].data_retrieval(**kwargs)
    if data:
        data = bunchify(json.loads(data))

    if device_id:
        device = [device for device in data.devices if device.id == device_id]
        if len(device) == 1:
            data = device
    else:
        data = data.devices

    return prepare_response(data)


@app.route('/devices/by-room/<int:room_id>', methods=['GET'])
@true_home_api(permission_needed=False)
def get_devices_in_room(room_id=None, **kwargs):
    kwargs.update({'room_id': room_id})
    data = VENDORS_API[VENDORS.Vera].data_retrieval(**kwargs)
    if data:
        data = bunchify(json.loads(data))

    if room_id:
        device = [device for device in data.devices if device.room == room_id]
        data = device

    return prepare_response(data)


@app.route('/devices/<int:device_id>/<status:status>', methods=['GET', 'PUT'])
@true_home_api(permission_needed=True)
def set_device_status(device_id, status):
    return prepare_response(VENDORS_API[VENDORS.Vera].data_manipulation(**{'device_id': device_id,
                                                                           'status': status}))


@app.route('/validate_connection', methods=['GET'])
@true_home_api(permission_needed=False)
def check_connection_home():
    return prepare_response(VENDORS_API[VENDORS.Vera].check_connectivity())


@app.route('/schedule/list_jobs', methods=['GET'])
@true_home_api(permission_needed=False)
def list_scheduled_jobs():
    jobs = get_scheduled_jobs()
    return prepare_response(jobs)


@app.route('/schedule/delete_job/cron/<int:job_id>', methods=['GET', 'PUT'])
@true_home_api(permission_needed=True)
def delete_cron_job_by_id(job_id):
    delete_cron_job(job_id)


@app.route('/schedule/delete_job/at/<int:job_id>', methods=['GET', 'PUT'])
@true_home_api(permission_needed=True)
def delete_at_job_by_id(job_id):
    success = delete_at_job(job_id)
    return 'Success!' if success else 'Failed :('
