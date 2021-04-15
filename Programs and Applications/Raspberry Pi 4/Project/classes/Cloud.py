import requests
import time
import json


def refresh_token(func):
    def wrapper(self, *args, **kwargs):
        if time.time() > self.access_token_expiration:
            self.update_token()
        res = func(self, *args, **kwargs)
        return res

    return wrapper


class Cloud(object):
    def __init__(self, my_id, my_secret):
        self.id = my_id
        self.secret = my_secret
        self.host = "https://iot.alticelabs.com/api/"
        self.access_token = None
        self.access_token_expiration = None
        self.update_token()

    # ------------ TOKEN ------------

    def update_token(self):
        print("Generating new token..")
        timer = 3500
        try:
            self.access_token = self.get_access_token()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            print(e)
        else:
            self.access_token_expiration = time.time() + timer
            print("New token:", self.access_token)

    def get_access_token(self):
        data = {
            "grant_type": "client_credentials"
        }
        directory = "devices/token"

        try:
            request = requests.post(
                self.host + directory,
                data=data,
                auth=(self.id, self.secret)
            )
        except Exception as e:
            print(e)
            return None
        else:
            return request.text

    # ------------ DATA ------------
    @refresh_token
    def post_data(self, stream_name, data_json, timestamp=None, ttl=300):
        directory = "/api/devices/{device_id}/streams/{stream_name}/value".format(
            device_id=self.id,
            stream_name=stream_name
        )
        stream_names = ["humidity", "temperature", "ergonomy_back", "ergonomy_seat", "cardiac_freq",
                        "respiratory_freq", "noise", "luminosity"]

        if stream_name not in stream_names:
            raise Exception("Stream requested doesn't exist")

        try:
            json.loads(data_json)
        except Exception as e:
            print(e)
        else:
            headers = {
                'Authorization': 'Bearer {}'.format(self.access_token),
                'Content-Type': 'application/json',
            }

            if timestamp is None:
                data = {
                    '{'
                    '"value": "{value}",'
                    '"ttl": {ttl}'
                    '}'.format(
                        value=data_json,
                        ttl=ttl
                    )
                }
            else:
                data = {
                    '{'
                    '"timestamp": "{timestamp}",'
                    '"value": "{value}",'
                    '"ttl": {ttl}'
                    '}'.format(
                        timestamp=timestamp,
                        value=data_json,
                        ttl=ttl
                    )
                }

            request = requests.post(
                self.host + directory,
                data=data,
                auth=(self.id, self.secret)
            )

            if request.status_code != 204:
                raise Exception("It was not possible to upload stream data")

        pass
