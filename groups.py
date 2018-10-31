from vkclass import VKUser
import json


def create_group_data(group):
    return {
        'name': group['name'],
        'gid': group['id'],
        'members_count': group['members_count']
    }


def write_file(result):
    with open('groups.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


def find_unique_groups():
    input_id = input('Введите ID пользователя: ')
    vk_user = VKUser(input_id)

    vk_user_groups = vk_user.get_groups()
    groups_list = set(vk_user_groups['response']['items'])

    if len(groups_list) > 0:

        vk_user_friends = vk_user.get_friends()
        friends_list = vk_user_friends['response']['items']

        if len(friends_list) > 0:
            friends_groups = set()

            for item, friend_id in enumerate(friends_list):
                response = VKUser(friend_id).get_groups()

                try:
                    friend_groups = response['response']['items']
                    friends_groups.update(friend_groups)
                    print(f'Обработано профилей друзей: {item + 1}, осталось: {len(friends_list) - item - 1}')

                except KeyError:
                    code = response['error']['error_msg']
                    if 'Access denied: this profile is private' in code:
                        print('Пользователь скрыл информацию')
                    elif 'User was deleted or banned' in code:
                        print('Пользователь удалён')
                    else:
                        print('Не удалось получить информацию о пользователе')

            common_groups = groups_list & friends_groups
            unique_groups = groups_list - common_groups

            result = list()

            unique_groups_data = vk_user.get_groups_data(unique_groups)['response']

            for group in unique_groups_data:
                try:
                    created_group_data = create_group_data(group)
                    result.append(created_group_data)
                except KeyError:
                    group_conflict = group['id']
                    print(f'Не удалось получить информацию о группе с ID {group_conflict} (группа удалена).')
            print(f'Всего уникальных групп: {len(result)}\nИнформация записана в файл groups.json.')

            write_file(result)

        else:
            print('У пользователя нет друзей')
            pass

    else:
        print('Пользователь не состоит в группах')
        pass


if __name__ == '__main__':
    find_unique_groups()
