#!/usr/local/python/bin
# --coding:utf-8--

import web
import redis
import math

urls = (
    '/', 'index',
    '/test', 'test',
)

app = web.application(urls, globals())

class index:
    def GET(self):


class test:
    def GET(self):
        print web.input()
        return '222'
if __name__ == "__main__":
    app.run()
