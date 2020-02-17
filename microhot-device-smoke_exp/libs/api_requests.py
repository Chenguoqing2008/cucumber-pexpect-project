import json
import time
import traceback
import requests
from libs.logging_conf import Logger


def api_get(call):
    max_tries = 2
    rs = None
    for retry in range(max_tries):
        try:
            rs = requests.get(call)
            rs = [rs, call]
            return rs if rs[0].status_code not in [500, 404] else \
                Logger.logger.info("get request failure.")
        except \
                (ValueError, requests.ConnectionError, requests.RequestException) as er:
            traceback.print_exc()
            Logger.logger.debug("failure message is {}".format(er))
            Logger.logger.debug(
                "GET request %s request failure and try again..." % call) if retry == 1 \
                else Logger.logger.error("request failure.")
            time.sleep(1)
    return rs


def api_post(call, payload, headers=None):
    if headers == None:
        headers = {'Content-Type': 'application/json'}
    rs = None
    payload = json.dumps(payload) if type(payload) == dict else payload
    try:
        rs = requests.post(call, data=payload, headers=headers)
        rs = [rs, call]
        Logger.logger.debug(call)
        if rs[0].status_code in [500, 404]:
            Logger.logger.error(">>>>>>>request failure<<<<<<<")

    except \
            (ValueError, requests.RequestException, requests.ConnectionError, requests.HTTPError) as request_err:
        traceback.print_exc()
        Logger.logger.debug("POST method call API {} failure.".format(request_err))
    return rs


def soft_api_post(call, payload, headers=None):
    if headers == None:
        headers = {'Content-Type': 'application/json'}
    rs = None
    payload = json.dumps(payload) if type(payload) == dict else payload

    rs = requests.post(call, data=payload, headers=headers)

    return rs


def api_put(call, payload):
    headers = {'content-type': 'application/json'}
    rs = ''
    try:
        counter = 0
        delay_flag = True
        rs = None
        while delay_flag:
            counter += 1
            if counter <= 6:
                rs = requests.put(call, data=payload, headers=headers)
                rs = [rs, call]
                Logger.logger.debug(call)

                if rs[0].status_code not in [409]:
                    delay_flag = False
                else:
                    Logger.logger.debug("409 error. Sleep 10 seconds and send again.")
                    time.sleep(10)
            else:
                delay_flag = False

        if rs[0].status_code in [500, 404]:
            Logger.logger.error("request failure")

    except \
            (ValueError, requests.RequestException, requests.ConnectionError, requests.HTTPError) as request_err:
        Logger.logger.debug("PUT method call API {} failure. ".format(request_err))
    return rs


def api_delete(call):
    counter = 0
    max_tries = 2

    rs = ''
    while counter < max_tries:
        try:
            rs = requests.delete(call)
            rs = [rs, call]
            if rs[0].status_code in [500, 404]:
                Logger.logger.error("request failure")
            counter = max_tries
        except \
                (ValueError, requests.RequestException, requests.ConnectionError, requests.HTTPError) as request_err:
            traceback.print_exc()
            Logger.logger.debug("DELETE method call API {} failure".format(request_err))
            if counter < max_tries:
                counter += 1
                Logger.logger.debug('DELETE: %s fail again...' % call)
                time.sleep(1)
            else:
                Logger.logger.error("request failure")
                return rs[0].status_code
            raise Exception('call failure')
    return rs


def json_file_to_string(file_location):
    with open(file_location) as json_data:
        json_data = json.load(json_data)
        return json.dumps(json_data)
