import aiohttp
import asyncio
import json

async def get_ddg_message(finput):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': 'text/event-stream',
        'Accept-Language': 'en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://duckduckgo.com/',
        'Content-Type': 'application/json',
        'Origin': 'https://duckduckgo.com',
        'Connection': 'keep-alive',
        'Cookie': 'dcm=1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'TE': 'trailers',
        'x-vqd-accept': '1',
        'Cache-Control': 'no-store',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://duckduckgo.com/duckchat/v1/status', headers=headers) as response:
            token = response.headers['x-vqd-4']
            headers['x-vqd-4'] = token
        
        url = 'https://duckduckgo.com/duckchat/v1/chat'
        data = {
            'model': 'gpt-3.5-turbo-0125',
            'messages': [
                {
                    'role': 'user',
                    'content': finput
                }
            ]
        }

        async with session.post(url, headers=headers, json=data) as response:
            text = await response.text()
            
    ret = ""
    for line in text.split("\n"):
        if len(line) > 0 and line[6] == '{':
            dat = json.loads(line[6:])
            if "message" in dat:
                ret += dat["message"].replace("\\n", "\n")

    return ret