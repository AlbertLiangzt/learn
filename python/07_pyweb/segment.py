#!/usr/local/src/bin/python
# -*- coding:utf-8 -*

import sys
# 加载路径，用于访问web模块
sys.path.append('../../')
import json
import math
import web

import jieba
#import jieba.posseg
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
		# 具体的页面 template/index.html 
		# 最后一个参数为空，表示请求到当前页面
		return render.index('null', 'null', '输入id', '')
	def POST(self):
		param = web.input()
		print '...post数据请求中...'
		content = param['item_id']

		# tfidf
		result_list = []
		for x, w in jieba.analyse.extract_tags(content, withWeight = True):
			result_list.append(':'.join([x, str(round(w, 3))]))
		res_str = '<br>'.join(result_list)
		print 'tf-idf: ', res_str

		# textrank
		result_textrank_list = []
		for x, w in jieba.analyse.textrank(content, withWeight = True):
			#print 'xxx: ', x
			#print 'www: ', w
			print '%s\t%s' % (x,w)
			result_textrank_list.append(':'.join([x, str(round(w, 3))]))

		result_textrank_str = '<br>'.join(result_textrank_list)
		print 'textrank: ', result_textrank_str

		if len(res_str) <=0 or len(result_textrank_str) <=0:
			return json.dumps({'block_one':'tfidf is null', 'block_two':'textrank is null'}, ensure_ascii = True, encoding = 'utf-8')
		else :
			return json.dumps({'block_one':res_str, 'block_two':result_textrank_str}, ensure_ascii = True, encoding = 'utf-8')


if __name__ == '__main__':
	app.run()
