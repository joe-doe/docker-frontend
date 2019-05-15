from flask_socketio import emit
import time
from pymongo import CursorType


def init_websockets(socketio, db):
    @socketio.on('get_logs')
    def logs_response():
        cursor = db.entry.find(cursor_type=CursorType.TAILABLE)
        while cursor.alive:
            try:
                change = next(cursor)
                del change['_id']
                emit('logs_response', {'data': str(change)})
            except StopIteration:
                time.sleep(1)
        print("CURSOR DEAD")

    @socketio.on('connect')
    def logs_connect():
        emit('logs_response', {'data': 'Connected'})

    @socketio.on('disconnect')
    def logs_disconnect():
        print('Client disconnected')
