import asyncio
from aiohttp import ClientSession
# import random

__MUSIC_NUM = 8  # hu 返回的最大歌曲数

async def __fetch(url,data,loop):
	try:
		async with ClientSession(loop=loop) as session:
			# hu 发送POST请求，data为POST请求参数，字典类型
			async with session.post(url, data=data,timeout=5) as response:
				# hu 以json格式读取响应的body并返回字典类型
				return await response.json()
	except Exception as ex:
		print('__fetch:%s' % ex)

async def getMusicInfo(keyword,offset, loop):
	global __MUSIC_NUM
	urlFace = 'http://s.music.163.com/search/get'
	dataMusic = {'type': '1',
				's': keyword,
				'limit': str(__MUSIC_NUM),
				'offset': str(offset)}
	result = None
	try:
		task = asyncio.ensure_future(__fetch(urlFace, dataMusic,loop),loop=loop)
		taskDone = await asyncio.wait_for(task,timeout=5)
		if 'result' not in taskDone:
			return result

		# random.shuffle(taskDone['result']['songs'])  # hu 打乱顺序
		for song in taskDone['result']['songs']:
			if result is None:
				result = [{'name':song['name'],
						   'artist':song['artists'][0]['name'],
						   'picUrl':song['album']['picUrl'],
						   'audio':song['audio'],
						   'page':song['page']}]
			else:
				result.append({'name': song['name'],
							   'artist': song['artists'][0]['name'],
							   'picUrl': song['album']['picUrl'],
							   'audio': song['audio'],
							   'page': song['page']})
	except Exception as ex:
		print('getMusicInfo:%s' % ex)
	return result

def __main():
	loop = asyncio.get_event_loop()
	music = '彩虹'
	player = '乔楚熙'
	task = asyncio.ensure_future(getMusicInfo(music+player,0,loop),loop=loop)
	taskDone = loop.run_until_complete(task)
	print(len(taskDone))
	for song in taskDone:
		print(song)
	loop.close()

if __name__ == '__main__':
	__main()
