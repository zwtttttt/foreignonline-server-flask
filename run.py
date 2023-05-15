# 创建应用实例
import sys

from flask_socketio import SocketIO
from wxcloudrun import app

# 创建 SocketIO 实例
socketio = SocketIO(app, path="/chat")

# 启动 Flask Web 服务
if __name__ == '__main__':
    socketio.run(app, host=sys.argv[1], port=sys.argv[2])
