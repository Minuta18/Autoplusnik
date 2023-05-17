# Autoplusnik Copyright (C) 2023 Igor Samsonov

import requests as rq
import time
import json

STANDART_HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
}
ALLOW_USER_DELETING = True

def get_auth_token(client_id, client_secret) -> str:
    '''Gets authentication token'''

    auth = rq.auth.HTTPBasicAuth(client_id, client_secret)
    token_response = rq.post('https://stepik.org/oauth2/token/', data={'grant_type': 'client_credentials'}, auth=auth).json()
    token = token_response.get('access_token', None)

    if not token:
        raise ValueError('Id or secret aren\'t correct')
    
    return token

def get_auth(headers: dict, token: str) -> dict:
    '''Creates headers with authentication'''
    return {'Authorization': 'Bearer ' + token, **headers}

def get_users(klass: int, token: str):
    '''Getting users'''

    user_list = [] # result

    has_next_page = False
    while not has_next_page:
        users = rq.get(f'https://stepik.org/api/students?klass={klass}&page=1', get_auth(STANDART_HEADERS, token)).json()
        for user in users['students']:
            user_list.append(user)

        has_next_page = users['meta']['has_next']

    return user_list

def refresh_all_rersults(klass: int, token: str):
    '''Updates users' results'''
    users = get_users(klass, token)

    for user in users:
        user_id = user['id']

        resp = rq.post(f'https://stepik.org/api/course-grades/{user_id}/refresh', get_auth(STANDART_HEADERS, token))

def download_last_report(klass: int, token: str): # TODO: add "save as" parameter
    '''Downloads last report'''
    information = rq.post(
        f'https://stepik.org/api/long-tasks', 
        data='{"longTask":{"type":"class_download_grade_book","klass":"' + str(klass) + '"}}', 
        headers=get_auth(STANDART_HEADERS, token)
    ).json()

    creating_data = rq.get(f"https://stepik.org/api/long-tasks/{ (information['long-tasks'][0]['id']) }", headers=get_auth(STANDART_HEADERS, token)).json()
    while creating_data['long-tasks'][0]['status'] != 'ready':
        # print(creating_data['long-tasks'][0]['status'])
        time.sleep(1)
        creating_data = rq.get(f"https://stepik.org/api/long-tasks/{ (information['long-tasks'][0]['id']) }", headers=get_auth(STANDART_HEADERS, token)).json()

    report_url = creating_data['long-tasks'][0]['result']['files'][1]['url']
    downloaded_report = rq.get(report_url).content

    with open('./last_report.xlsx', 'wb') as f:
        f.write(downloaded_report)

def update(client_id, client_secret, klass):
    token = get_auth_token(client_id, client_secret)
    refresh_all_rersults(klass, token)
    download_last_report(klass, token)
    print('Updated')