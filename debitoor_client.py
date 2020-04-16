import webbrowser

import requests


class ApiError(Exception):
    pass


class DebitoorClient:
    BASE_URL = "https://app.debitoor.com"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.headers = None

    def use_access_token(self, access_token):
        headers = {
            "x-token": access_token
        }
        resp = requests.get(self.BASE_URL + "/api/environment/v1?token=" + access_token, headers)

        if resp.status_code != 200:
            raise ApiError("Invalid Access Token")

        self.access_token = access_token
        self.headers = headers

    def request_access_token(self, code: str):
        data = {
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": "https://syscy.de/debitoor/oauth.php"
        }
        resp = requests.post(self.BASE_URL + "/login/oauth2/access_token", json=data)

        if resp.status_code != 200:
            raise ApiError("POST /login/oauth2/access_token {}".format(resp.status_code))

        access_token = resp.json()["access_token"]

        self.use_access_token(access_token)
        print("Auth successful!")

        return access_token

    def open_oauth_page(self):
        webbrowser.open_new(
            "https://app.debitoor.com/login/oauth2/authorize?client_id=" + self.client_id + "&response_type=code")

    def list_customers(self):
        resp = requests.get(self.BASE_URL + "/api/customers/v2", self.headers)

        if resp.status_code != 200:
            raise ApiError("GET /api/customers/v2 {}".format(resp.status_code))

        return resp.json()
