import requests
import time

API_URL = 'https://api.vk.com/method'
TOKEN = '1eb685ead2be7761e98170d3be803e824206d523ccc7c2f2fe9b7ff562ced6dc0b60fb1c9b0981d847b41'
VERSION = '5.85'


class VKUser:

    def __init__(self, input_id):
        user_id = str(input_id)
        if user_id.isdigit() is False:
            params_init = dict(access_token=TOKEN, user_ids=input_id, v=VERSION)
            method_url = f'{API_URL}/users.get'
            request_id = requests.get(method_url, params_init).json()['response'][0]['id']
            self.user_id = request_id
        else:
            self.user_id = input_id

    def get_get_request(self, method_name):
        method_url = f'{API_URL}/{method_name}'
        params_get_request = dict(access_token=TOKEN, user_id=self.user_id, v=VERSION)
        result = requests.get(method_url, params=params_get_request).json()
        time.sleep(0.4)
        return result

    def get_friends(self):
        method_url = f'{API_URL}/friends.get'
        params_get_friends = dict(access_token=TOKEN, user_id=self.user_id, v=VERSION)
        result = requests.get(method_url, params_get_friends).json()
        return result

    def get_groups(self):
        method_url = f'{API_URL}/groups.get'
        params_get_groups = dict(access_token=TOKEN, user_id=self.user_id, v=VERSION)
        result = requests.get(method_url, params_get_groups).json()
        return result

    def get_groups_data(self, group_ids):
        method_url = f'{API_URL}/groups.getById'
        params_groups_data = dict(access_token=TOKEN, fields='members_count', v=VERSION)
        params_groups_data['group_ids'] = ','.join(map(str, group_ids))
        result = requests.get(method_url, params_groups_data).json()
        time.sleep(0.4)
        return result
