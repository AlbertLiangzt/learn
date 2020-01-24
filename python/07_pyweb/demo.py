#!/usr/local/src/bin/python
# -*- coding:utf-8 -*

import sys
# 加载路径，用于访问web模块
sys.path.append('../../')
import json
import math
import web


urls = (
	'/', 'index',
	'/test', 'test',
)

render = web.template.render('template/')
web.template.Template.globals['render'] = render

config = web.storage (
	static = '/static',
	resource = '/resource'
)

web.template.Template.globals['config'] = config

app = web.application(urls, globals())

# urls中输入的访问路径，指向对应的class
# ip:port/url
class test:
	def GET(self):
		ret = 'test page'
		return ret

test_dict = {'aaa':'111', 'bbb':'222', 'ccc':'333'}
test2_dict = {'aaa':'111', 'bbb':'222', 'ccc':'444'}

class index:
	def GET(self):
		print '...页面初始化中...'
		# 具体的页面 template/index.html 
		# 最后一个参数为空，表示请求到当前页面
		return render.index('null', 'null', '输入id', '')
	def POST(self):
		param = web.input()
		print '...post数据请求中...'
		item_id = param['item_id']
		print 'id: '+item_id
		if item_id not in test_dict:
			return json.dumps({'block_one':'not in test_dict', 'block_two':'not in test2_dict'}, ensure_ascii = True, encoding = 'utf-8')
		else :
			print 'block_one: ' + test_dict[item_id]
			print 'block_two: ' + test2_dict[item_id]
			return json.dumps({'block_one':test_dict[item_id], 'block_two':test2_dict[item_id]}, ensure_ascii = True, encoding = 'utf-8')

if __name__ == '__main__':
	app.run()
