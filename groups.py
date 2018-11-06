from vkclass import VKUser
import json
import time
import sys


def check_validity(input_id):
    try:
        VKUser(input_id)
    except KeyError:
        sys.exit('Данные введены неверно')


def get_user_groups(input_id):
    vk_user_groups = VKUser(input_id).get_groups()
    groups_list = set(vk_user_groups['response']['items'])
    return groups_list


def get_user_friends(input_id):
    vk_user_friends = VKUser(input_id).get_friends()
    return vk_user_friends['response']['items']


def get_friends_groups(friends_list):
    friends_groups = set()

    for item, friend_id in enumerate(friends_list):
        try:
            response = VKUser(friend_id).get_groups()
        except RuntimeError:
            time.sleep(0.35)
        try:
            friend_groups = response['response']['items']
            friends_groups.update(friend_groups)
            print(f'Обработано профилей друзей: {item + 1}, осталось: {len(friends_list) - item - 1}')
        except KeyError:
            code = response['error']['error_code']
            if code == 15:
                print('Пользователь скрыл информацию')
            elif code == 18:
                print('Пользователь удалён')
            else:
                print('Не удалось получить информацию о пользователе')
    return friends_groups


def create_group_data(group):
    return {
        'name': group['name'],
        'gid': group['id'],
        'members_count': group['members_count']
    }


def prepare_data(input_id, unique_groups):
    result = list()

    unique_groups_data = VKUser(input_id).get_groups_data(unique_groups)['response']

    for group in unique_groups_data:
        try:
            created_group_data = create_group_data(group)
            result.append(created_group_data)
        except KeyError:
            group_conflict = group['id']
            print(f'Не удалось получить информацию о группе с ID {group_conflict} (группа удалена).')
    return result


def write_file(result):
    with open('groups.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


def find_unique_groups():
    input_id = input('Введите ID пользователя: ')
    check_validity(input_id)
    groups_list = get_user_groups(input_id)
    print('Получен список групп пользователя')

    if len(groups_list) > 0:
        friends_list = get_user_friends(input_id)
        print('Получен список друзей пользователя')

        if len(friends_list) > 0:
            friends_groups = get_friends_groups(friends_list)
            common_groups = groups_list & friends_groups
            unique_groups = groups_list - common_groups
            print('Получен список уникальных групп')

            result = prepare_data(input_id, unique_groups)
            write_file(result)
            print(f'Всего уникальных групп: {len(result)}\nИнформация записана в файл groups.json.')

        else:
            print('У пользователя нет друзей')
            pass

    else:
        print('Пользователь не состоит в группах')
        pass


if __name__ == '__main__':
    find_unique_groups()

