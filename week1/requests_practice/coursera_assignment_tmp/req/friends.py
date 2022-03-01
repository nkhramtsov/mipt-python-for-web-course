import datetime
from typing import List

import requests

ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
API_VERSION = '5.131'
NOW = datetime.datetime.now().year


def get_id_by_username(username: str) -> int:
    params = {'v': API_VERSION, 'access_token': ACCESS_TOKEN, 'user_ids': username}
    response = requests.get('https://api.vk.com/method/users.get', params=params)
    return response.json()['response'][0]['id']


def get_friends_by_id(vk_id: int) -> dict:
    params = {'v': API_VERSION, 'access_token': ACCESS_TOKEN, 'user_id': vk_id, 'fields': 'bdate'}
    response = requests.get('https://api.vk.com/method/friends.get', params=params)
    return response.json()


def parse_friends_response(friends_response: dict) -> List[int]:
    parsed_data = {}
    for friend in range(friends_response['response']['count']):
        if 'bdate' in friends_response['response']['items'][friend]:
            friend_bdate = friends_response['response']['items'][friend]['bdate']
            if len(friend_bdate) > 5:
                age = get_age_from_bdate(friend_bdate)
                parsed_data[age] = parsed_data.get(age, 0) + 1
    return sorted(parsed_data.items(), key=lambda x: (-x[1], x[0]))


def get_age_from_bdate(bdate: str) -> int:
    birth_year = int(bdate.split('.')[-1])
    age = NOW - birth_year
    return age


def calc_age(uid: str) -> List[int]:
    if not uid.isnumeric():
        uid = get_id_by_username(uid)
    friends_dict = get_friends_by_id(uid)
    age = parse_friends_response(friends_dict)
    return age


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
