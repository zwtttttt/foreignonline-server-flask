from flask import Flask
from flask_sockets import Sockets
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/chat')
def chat(ws):
    while not ws.closed:
        message = ws.receive()
        if message:
            # 处理接收到的消息
            response = {
                'result': 'received message: {}'.format(message)
            }
            ws.send(response)

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
