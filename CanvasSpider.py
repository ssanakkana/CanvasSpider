import requests
import os
import json

headers = {
        'Cookie': 'log_session_id=ff253a9db71633269a1f51b9aeb5a038; _legacy_normandy_session=zJjJECWpGJ6mPFMRGI5heA+q8J_h6BSzR-M9mA5iQ3rn2_ujvYVNbzn0xtWa1jzGVme8GaiO_WIu42hCPkfW6vE61wzmzN2G6Rez2JdiOEfsFBmcI37erSu2Wqs8py3zP0Wnvtxq1tDqgQ5cII8oRgMXfmdFaSu8wCYugRYKyuOyCyHr2uEd1w_nQg1EnqeE5Jk0-h_JY7uc5nNMyXpXXdw0pS-WaXPSe2gq2ghSBUU-rR5XYsO73tDnigLA7R9PhzKzWPXpyFs_7J5TcOWfFB5xgCpS119ZLADr5Yv-LM0BtEsFHUa5DHNPBQsSVYPT3-UOKOFbk-kSCTbQJcKVRBx3LdgyV5E6Y5KS3k70b9QSVYj78yCMCidI9HWb3GlOeG7dALIY7o0beegX4NzVmvY6o70Fm0wMaLLZ5vqm5PSCg.wVOvH1MqY-X2UtZZZpxkaOBGbSk.ZbEoyw; _csrf_token=%2F%2Flb2eVTXZuXV%2BlYz%2BdDf3U1Nzn5%2F8OQg8hzTil1lXeKyRHqjTcq7uMmvhGttXY2Rwx6fsGGicnQgRQEETf7Pw%3D%3D',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Hos': 'jicanvas.com',
        'X-Requested-With': 'XMLHttpRequest'
    }


def get_page(offset):
    url = f'https://jicanvas.com/api/v1/courses/124/discussion_topics?only_announcements=true&per_page=40&page={offset}&filter_by=all&no_avatar_fallback=1&include[]=sections_user_count&include[]=sections'
    try:
        response = requests.get(url, headers=headers)
        response.close()
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print("ConnectionError")
            print(response.status_code)
    except requests.ConnectionError:
        return None


def get_info(item):
    info = item.get('author')
    annoucement_id = item.get('id')
    avatar_image_url = info.get('avatar_image_url')
    name = info.get('display_name')
    return {
        'id': annoucement_id,
        'title': item.get('title'),
        'avatar_image_url': avatar_image_url,
        'name': name
    }


def save_info(item):
    file_path = item.get('id')
    url = item.get('avatar_image_url')
    if not os.path.exists('Announcement'):
        os.mkdir('Announcement')
    if not os.path.exists(f'.//Announcement//{file_path}'):
        os.mkdir(f'.//Announcement//{file_path}')
    else:
        print('Already Downloaded, id =', item.get('id'))
        return
    if url is not None:
        try:
            response = requests.get(item.get('avatar_image_url'), headers=headers)
            response.close()
            if response.status_code == requests.codes.ok:
                with open(f'.//Announcement//{file_path}//{file_path}.jpg', 'wb') as f:
                    f.write(response.content)
        except requests.ConnectionError:
            print('Failed to Save Info')
    with open(f'.//Announcement//{file_path}//{file_path}.json', 'w') as f:
        f.write(json.dumps(item))


def main(offset):
    js = get_page(offset)
    for item in js:
        info = get_info(item)
        save_info(info)


PAGE_START = 1
PAGE_END = 2

if __name__ == '__main__':
    for x in range(PAGE_START, PAGE_END + 1):
        main(x)
