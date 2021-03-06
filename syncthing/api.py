from flask import abort, jsonify, request
from flask.views import MethodView

from . import backend


class SyncthingFoldersAPI(MethodView):
    def get(self, id=None):
        folders = backend.get_repos(id)
        if id and not folders:
            abort(404)
        if type(folders) == list:
            return jsonify(folders=folders)
        else:
            return jsonify(folder=folders)

    def post(self):
        data = request.get_json()["folder"]
        folder = backend.add_repo(
            data["id"], data["path"], data["read_only"], data["ignore_perms"],
            data["keep_versions"] if data["versioning"] else False,
            data["rescan_interval_s"], data["devices"])
        return jsonify(folder=folder)

    def put(self, id=None):
        if not id:
            abort(422)
        data = request.get_json()["folder"]
        folder = backend.edit_repo(
            data["id"], data["path"], data["read_only"], data["ignore_perms"],
            data["keep_versions"] if data["versioning"] else False,
            data["rescan_interval_s"], data["devices"])
        return jsonify(folder=folder)

    def delete(self, id=None):
        if not id:
            abort(422)
        backend.del_repo(id)
        return jsonify(), 204


class SyncthingDevicesAPI(MethodView):
    def get(self, id=None):
        devices = backend.get_nodes(id)
        if id and not devices:
            abort(404)
        if type(devices) == list:
            return jsonify(devices=devices)
        else:
            return jsonify(device=devices)

    def post(self):
        data = request.get_json()["device"]
        device = backend.add_device(
            data["name"], data["device_id"], list(data["addresses"])
            if not type(data["addresses"]) == list else data["addresses"]
        )
        return jsonify(device=device)

    def put(self, id=None):
        if not id:
            abort(422)
        data = request.get_json()["device"]
        device = backend.edit_node(data)
        return jsonify(device=device)

    def delete(self, id):
        if not id:
            abort(422)
        backend.del_node(id)
        return jsonify(), 204


def config():
    if request.method == "GET":
        return jsonify(
            myid=backend.get_myid(), config=backend.pull_config()
        )
    else:
        config = request.get_json()["config"]
        return jsonify(
            myid=backend.get_myid(), config=backend.save_config(config)
        )


folders = SyncthingFoldersAPI.as_view('syncfolders_api')
devices = SyncthingDevicesAPI.as_view('syncdevices_api')
