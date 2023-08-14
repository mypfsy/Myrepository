import os
import time

import requests
import aiohttp
import asyncio
import aiofiles
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad




def get_m3u8_urls_text(index_m3u8_url):
    m3u8_urls_text_resp = requests.get(index_m3u8_url).text
    with open('m3u8_urls.text', 'w', encoding='utf-8')as f:
        f.write(m3u8_urls_text_resp)


def gte_urls_list():
    f = open('m3u8_urls.text', 'r', encoding='utf-8')
    m3u8_urls_list = []
    while 1:
        line = f.readline()
        if not line:
            break
        if line[0]=='#':
            continue
        m3u8_urls_list.append(line.split('/')[-1])
    f.close()
    return m3u8_urls_list


def get_file_txt(m3u8_urls):
    ff = open('file.txt', 'w', encoding='utf-8')
    for i in m3u8_urls:
        s = 'file' + ' ' + f'temp_{i.strip()}' + '\n'
        ff.write(s)
    ff.close()


async def aio_get_m3u8_video(m3u8_urls_list, m3u8_url_http):
    tasks = []
    for m3u8_url_data in m3u8_urls_list:
        tasks.append(asyncio.create_task(get_m3u8_video(m3u8_url_http, m3u8_url_data)))
    await asyncio.wait(tasks)


async def get_m3u8_video(m3u8_url_http, m3u8_url_data):
    try:
        timeout = aiohttp.ClientTimeout(total=300)
        name = m3u8_url_data.split(".")[0]
        m3u8_url = f'{m3u8_url_http}/{m3u8_url_data}'
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(m3u8_url) as m3u8_video_resp:
                with open(f'{name}' + '.ts', 'wb') as m3u8:
                    m3u8.write(await m3u8_video_resp.content.read())
                    print(1, '...', name)

    except:
        try:
            timeout = aiohttp.ClientTimeout(total=300)
            name = m3u8_url_data.split(".")[0]
            m3u8_url = f'{m3u8_url_http}/{m3u8_url_data}'
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(m3u8_url) as m3u8_video_resp:
                    with open(f'{name}' + '.ts', 'wb') as m3u8:
                        m3u8.write(await m3u8_video_resp.content.read())
                        print(2, '...', name)
        except:
            timeout = aiohttp.ClientTimeout(total=3000)
            name = m3u8_url_data.split(".")[0]
            m3u8_url = f'{m3u8_url_http}/{m3u8_url_data}'
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(m3u8_url) as m3u8_video_resp:
                    with open(f'{name}' + '.ts', 'wb') as m3u8:
                        m3u8.write(await m3u8_video_resp.content.read())
                        print(3, '...', name)


def get_key_text(key_url):
    key = requests.get(key_url).text
    key = key.encode('utf-8')
    return key


async def aio_decode_m3u8_video(m3u8_urls_list, key):
    tasks = []
    for m3u8_video in m3u8_urls_list[4000:]:
        m3u8_video = m3u8_video.strip()
        tasks.append(asyncio.create_task(decode_m3u8_video(m3u8_video, key)))
    await asyncio.wait(tasks)


async def decode_m3u8_video(m3u8_video, key):
    aes = AES.new(key=key, IV=b'0000000000000000', mode=AES.MODE_CBC)
    async with aiofiles.open(f'{m3u8_video}', 'rb') as video:
        async with aiofiles.open(f'temp_{m3u8_video}', 'wb') as ts:
            video_data = await video.read()
            if len(video_data) % 16 != 0:
                video_data = pad(video_data, 16)
            await ts.write(aes.decrypt(video_data))
            video.close()
            ts.close()


def m3u8_to_mp4():
    os.system('ffmpeg -f concat -i file.txt -c copy output.mp4')


# def get(m3u8_urls_list, m3u8_url_http):
#     for name in m3u8_urls_list:
#         name = name.strip()
#         if os.path.exists(name):
#             continue
#         with open(f'{name}', 'wb') as f:
#             f.write(requests.get(f'{m3u8_url_http}/{name}').content)
#             print('c', '...', name)


def main(m3u8_url_http):
    key_url = f'{m3u8_url_http}/key.key'
    index_m3u8_url = f'{m3u8_url_http}/index.m3u8'
    get_m3u8_urls_text(index_m3u8_url)
    print('已获取', 'm3u8_urls.text')
    m3u8_urls_list = gte_urls_list()
    print('已获取', 'm3u8_urls_list')
    get_file_txt(m3u8_urls_list)
    print('已获取', 'file.txt')
    print(f'共 {len(m3u8_urls_list)} 个', 'ts')
    asyncio.run(aio_get_m3u8_video(m3u8_urls_list, m3u8_url_http))
    print('已获取', 'm3u8_video')
    # get(m3u8_urls_list, m3u8_url_http)
    key = get_key_text(key_url)
    print('已获取', 'key')
    asyncio.run(aio_decode_m3u8_video(m3u8_urls_list, key))
    print('已解密', 'm3u8_video')
    m3u8_to_mp4()
    print('已合成', 'output.mp4')
    os.remove('m3u8_urls.text')
    os.remove('file.txt')
    print('已删除', 'm3u8_urls.text, file.txt')
    for name in m3u8_urls_list:
        os.remove(f'{name.strip()}')
        os.remove(f'temp_{name.strip()}')
    print('已删除所有 ts 文件')


if __name__ == '__main__':

    m3u8_url_http = ''
    main(m3u8_url_http)


