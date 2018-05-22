import redis
import time


class RedisClient(object):

	def __init__(self):
		self._db = redis.Redis(host='', port=6379, password='txfredis')

	def get_proxy(self):
		# 取出代理
		try:
			proxy = self._db.rpop('proxies').decode('utf-8')
			if isinstance(proxy, bytes):
				proxy = proxy.decode('utf-8')
			return 'http://' + proxy
		except:
			print('proxy is empty sleep 5')
			time.sleep(5)

	def add_movie_id(self, id):
		return self._db.sadd('movie_id', id)

	def add_movie_url(self, url):
		self._db.sadd('movie_url', url)

	def pop_movie_url(self):
		url = self._db.spop('movie_url')
		if isinstance(url, bytes):
			url = url.decode('utf-8')
		return url

redis_db = RedisClient()