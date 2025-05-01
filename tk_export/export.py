import typing

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
    settings: structs.Settings
    _session = None

    def __init__(self, settings: structs.Settings) -> None:
        self.settings = settings
        self._session = requests.Session()

    def _call_api(self, method: str, url: str, params: dict) -> dict:
        req = requests.Request(method, url, headers=HEADERS, cookies=self.settings.cookie, params=params)

        resp = self._session.send(req.prepare())
        if resp.status_code != 200:
            print(f"error: {resp.status_code}: {resp.text}")
            return {}

        return resp.json()

    def _call_api_paginate(self, method: str, url: str, params: dict) -> dict:
        data = self._call_api(method, url, params)
        if data.get('pages', 0) > 1:
            params = {}
            for page in range(2, data['pages'] + 1):
                params['page'] = page
                resp = self._call_api(method, url, params)
                data = _merge_dicts(data, resp)

        return data

    def get_campaign_list(self) -> typing.List[structs.Campaign]:
        endpoint = f"{HOST}/api_v0/users/{self.settings.user_id}/campaigns"
        api_response = self._call_api_paginate('GET', endpoint, {})

        response = [structs.Campaign.from_json(data) for data in api_response['campaigns']]

        return response

    def get_roleplays(self, campaign_id: int) -> typing.List[structs.Roleplay]:
        endpoint = f"{HOST}/api_v0/campaigns/{campaign_id}/roleplays"
        api_response = self._call_api_paginate('GET', endpoint, {})
        response = [structs.Roleplay.from_json(data) for data in api_response['roleplays']]

        return response

    def get_roleplay_messages(self, roleplay_id: int) -> typing.List[structs.RoleplayMessage]:
        endpoint = f"{HOST}/api_v0/roleplays/{roleplay_id}/messages"

        api_response = self._call_api_paginate('GET', endpoint, {})
        response = [structs.RoleplayMessage.from_json(data) for data in api_response['messages']]

        return response


if __name__ == '__main__':
    cookie = {'tavern-keeper': 'L1V2QlN3bVNRUVZibEE3dlNHWVRxVnhtQ2tzQnNSMStVbmhFa3hkalY5ck1oT0x2bU9rb1pRWmVTZVprOGlJdStnLzF2Y2NjL1ZmbHArYnkzUExSSUdNdXpyV2x2YVhUUUdvUkNSbDN2NFA2blphUDhOUHpFZUpHQS9KQnIyanBid3ZpYUIxOFJaYmF1Y2dHMDkwUkpWODA5SWthQVVhMmlYdTZlRURIS0xIRG5IRWhrNHM0QWg5cjFqcWE1a25yLS1Ed09RZUtyTHlOVnE5a1lLZks4b2FRPT0%3D--91cc8b9dbd6921a25008d417dcde886f94ecb2f0'}
    settings = structs.Settings(
        user_id="18650",
        cookie=cookie,
        campaigns=[]
    )

    client = TavernKeeperClient(settings)
    campaigns = client.get_campaign_list()
    for campaign in campaigns:
        print(campaign.name)
        for roleplay in client.get_roleplays(campaign.id):
            print(roleplay.name)
            for message in client.get_roleplay_messages(roleplay.id):
                print(message.content)