#!/usr/bin/python
import json
import threading
from mod_pywebsocket import msgutil
from wptserve import stash

address, authkey = stash.load_env_config()
path = "/stash_responder_blocking"
stash = stash.Stash(path, address=address, authkey=authkey)
cv = threading.Condition()

def handle_set(key, value):
    with cv:
      stash.put(key, value)
      cv.notify_all()

def handle_get(key):
    with cv:
        while True:
            value = stash.take(key)
            if value is not None:
                return value
            cv.wait()

def web_socket_do_extra_handshake(request):
    pass

def web_socket_transfer_data(request):
    line = request.ws_stream.receive_message()

    query = json.loads(line)
    action = query["action"]
    key = query["key"]
    response = {"success": True}

    if action == "set":
        value = query["value"]
        handle_set(key, value)
    elif action == "get":
        value = handle_get(key)
        response["value"] = value
    else:
        response["success"] = False

    msgutil.send_message(request, json.dumps(response))
