import requests
from database import Database


def get_pic(url):
	pic_name = url[46:]
	r = requests.get(url, stream=True)
	print(url, pic_name, r.status_code)
	if  r.status_code== 200:
		open('./hero_pic/' + pic_name, 'wb').write(r.content) # 将内容写入图片
	return


db = Database()
sql = "SELECT * FROM heroes;"
res = db.c.execute(sql)
for row in res:
	get_pic(row[3])
