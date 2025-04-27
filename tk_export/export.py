import requests

import structs

HOST = 'https://www.tavern-keeper.com'
HEADERS = {'accept': 'application/json', 'X-CSRF-Token': 'something'}

def _merge_dicts(original: dict, update: dict) -> dict:
    combined = original.copy()
    for key, value in update.items():
        if isinstance(value, list) and key in combined and isinstance(combined[key], list):
            combined[key].extend(value)
        else:
            combined[key] = value

    return combined


class TavernKeeperClient:
    settings: structs.settings
    _session = None

    def __init__(self, settings: structs.settings) -> None:
        self.settings = settings
        self._session = requests.Session()

    def _call_api(self, method: str, url: str, params: dict) -> dict:
        req = requests.Request(method, url, headers=HEADERS, params=params)

        resp = self._session.send(req.prepare())
        if resp.status_code != 200:
            return {}

        return resp.json()

    # unfinished
    def _call_api_paginate(self, method: str, url: str, params: dict) -> dict:
        data = self._call_api(method, url, params)
        if data.get('pages', 0) > 1:
            params = {}
            for page in range(2, data['pages'] + 1):
                params['page'] = page
                resp = self._call_api(method, url, params)