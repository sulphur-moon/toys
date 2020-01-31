# encoding:utf-8
import configparser
import requests
import base64
import time


'''
Token类
用来获取调用API的token
'''
class Token:
	def __init__(self, refresh=False):
		config = configparser.ConfigParser()
		file = 'config.ini'
		config.read(file)
		
		def get_new_token():
			AK = config.get('AppKey', 'AK')
			SK = config.get('AppKey', 'SK')
			print('refresh\tAK =', AK, '\tAK =', SK)
			host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='
			url = host + AK + '&client_secret=' + SK
			response = requests.get(url)
			# 如果有返回
			if response:
				json = response.json()
				token = json['access_token']
				expires = json['expires_in']
				print('access_token =', token, '\texpires_in =', expires)
				self.token = token
				timestamp = time.time()
				expired_time = int(timestamp) + int(expires) - 1
				config.set('Token', 'access_token', token)
				config.set('Token', 'expired_time', str(expired_time))
				with open(file,'w') as configfile:
					config.write(configfile)
			else:
				print('No response!')
				self.token = None
		
		# 如果强制刷新
		if refresh:
			get_new_token()
		else:
			# 如果token过期
			token = config.get('Token', 'access_token')
			expired_time = config.get('Token', 'expired_time')
			if not token or not expired_time or float(expired_time) < time.time():
				get_new_token()
			else:
				self.token = token
				print('access_token =', token, '\texpires_in =', expired_time, '\tnow =', time.time())
		return
	
	def get_token(self):
		return self.token

'''TSET
token = Token()
print(token.get_token())
'''


'''
OCR类
用来进行文字识别
'''
class OCR:
	def __init__(self):
		self.request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
		token = Token()
		self.access_token = token.get_token()
		return
	
	def get_response(self, filename):
		f = open(filename, 'rb')
		img = base64.b64encode(f.read())
		params = {"image":img}
		url = self.request_url + "?access_token=" + self.access_token
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		response = requests.post(url, data=params, headers=headers)
		if response:
			return response.json()
		else:
			return None
	
	def get_result(self, filename):
		json = get_response(filename)
		return json['words_result']

'''TEST
'''
ocr = OCR()
print(ocr.get_response('test.jpg'))