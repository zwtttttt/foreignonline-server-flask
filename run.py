# 创建应用实例
import sys

from wxcloudrun import app

# 启动Flask Web服务
if __name__ == '__main__':
    from flask import Flask
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    app = Flask(__name__)
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app, handler_class=WebSocketHandler)
    server.serve_forever()
