from datetime import datetime
from flask import render_template, request, Response, jsonify
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

import requests
from flask_cors import CORS
from flask_sockets import Sockets
sockets = Sockets(app)
CORS(app)

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)



@app.route('/chat/<string:message>', methods=['POST'])
def chat(message: str):
    url = "http://danto.cloud:12138/api/chat"
    headers = {"Content-Type": "application/json"}

    data = {
        'message': message,
        # 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
        # 'apiKey': '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'
    }
    

    def generate():
        with requests.post(url, headers=headers, json=data, stream=True) as response:
            for chunk in response.iter_content(chunk_size=1024):
                yield chunk.decode()

    return Response(generate(), content_type='text/event-stream')


@sockets.route('/')
def ws(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)
