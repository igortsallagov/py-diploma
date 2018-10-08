from vkclass import VKUser
import json
import time

def create_group_data(group):
    return {
        'name': group['name'],
        'gid': group['id'],
        'members_count': group['members_count']
    }


def write_file(result):
    with open('groups.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


def core():
    input_id = input('Введите ID пользователя: ')
    vk_user = VKUser(input_id)
    vk_user_friends = vk_user.get_friends()
    friends_list = vk_user_friends['response']['items']

    vk_user_groups = vk_user.get_groups()
    groups_list = set(vk_user_groups['response']['items'])
    time.sleep(0.4)

    friends_groups = set()

    for item, friend_id in enumerate(friends_list):
        progress = round(item / len(friends_list) * 100, 2)
        print(f'Обработка данных: {progress}')

        response = VKUser(friend_id).get_groups()

        try:
            friends_groups = set(response['response']['items'])
            friends_groups.update(friends_groups)
        except:
            'do nothing'
    time.sleep(0.4)
    common_groups = groups_list & friends_groups
    unique_groups = groups_list - common_groups
    result = list()

    unique_groups_data = vk_user.get_groups_data(unique_groups)['response']

    for group in unique_groups_data:
        created_group_data = create_group_data(group)
        result.append(created_group_data)

    write_file(result)


if __name__ == '__main__':
    core()