from flask import render_template, request
from flask_socketio import emit, join_room, leave_room
from app import app, socketio

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@socketio.on('join_room')
def on_join_room(data):
    room = data['room']
    join_room(room)
    emit('joined_room', {'room': room})

@socketio.on('leave_room')
def on_leave_room(data):
    room = data['room']
    leave_room(room)
    emit('left_room', {'room': room})

@socketio.on('message')
def on_message(data):
    emit('message', data, broadcast=True)
