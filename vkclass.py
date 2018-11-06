import requests

API_URL = 'https://api.vk.com/method'
VERSION = '5.85'
TOKEN = input('Введите токен: ')


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

    def get_friends(self):
        method_url = f'{API_URL}/friends.get'
        params_get_friends = dict(access_token=TOKEN, user_id=self.user_id, v=VERSION)
        result = requests.get(method_url, params_get_friends).json()
        return result

    def get_groups(self):
        method_url = f'{API_URL}/groups.get'
        params_get_groups = dict(access_token=TOKEN, user_id=self.user_id, count=1000, v=VERSION)
        result = requests.get(method_url, params_get_groups).json()
        return result

    def get_groups_data(self, group_ids):
        method_url = f'{API_URL}/groups.getById'
        params_groups_data = dict(access_token=TOKEN, fields='members_count', v=VERSION)
        params_groups_data['group_ids'] = ','.join(map(str, group_ids))
        result = requests.get(method_url, params_groups_data).json()
        return result
