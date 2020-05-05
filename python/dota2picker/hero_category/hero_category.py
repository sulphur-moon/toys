#coding=utf-8
import random
import json


strength = []
agility = []
intelligence = []
with open('strength', 'r', encoding='UTF-8') as f:
	content = f.read()
	strength = content.split('\n')
	print(strength)
	random.shuffle(strength)
	print(strength)
	strength = sorted(strength)
	print(strength)
with open('agility', 'r', encoding='UTF-8') as f:
	content = f.read()
	agility = content.split('\n')
	print(agility)
with open('intelligence', 'r', encoding='UTF-8') as f:
	content = f.read()
	intelligence = content.split('\n')
	print(intelligence)

with open('hero_category.js', 'w', encoding='UTF-8') as f:
	f.write("const strength = ")
	f.write(json.dumps(strength, ensure_ascii=False))
	f.write('\n')
	f.write("const agility = ")
	f.write(json.dumps(agility, ensure_ascii=False))
	f.write('\n')
	f.write("const intelligence = ")
	f.write(json.dumps(intelligence, ensure_ascii=False))
	f.write('\nexport {strength, agility, intelligence}')
	f.close()