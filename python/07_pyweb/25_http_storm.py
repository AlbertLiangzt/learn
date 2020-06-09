#!/usr/local/src/bin/python
# -*- coding:utf-8 -*

import sys
# 加载路径，用于访问web模块
sys.path.append('../../')
import json
import math
import web

import jieba
import jieba.analyse

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
		params = web.input()
		content = params.get('content', '')
		
		result_list = []
		for x,w in jieba.analyse.extract_tags(content, withWeight=True):
			result_list.append(':'.join([x, str(round(w,3))]))	
		
		res_str = ' '.join(result_list)
		print 'res_str: ', res_str

		return res_str

if __name__ == '__main__':
	app.run()
