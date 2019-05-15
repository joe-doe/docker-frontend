"""


"""
import os
from flask import Flask
from routes.routes import init_routes
from build_image.build_image import ImageHandler
from start_container.start_container import ContainersHandler
from monitoring.monitoring import Monitor
from database.database import get_db
from flask_socketio import SocketIO
from websocks.websocks import init_websockets

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.secret_key = os.urandom(24)

socketio = SocketIO(app)
db = get_db()
image_builder = ImageHandler()
containers_handler = ContainersHandler(db)
monitor = Monitor(containers_handler)

init_routes(app, image_builder, containers_handler, monitor)
init_websockets(socketio, db)


if __name__ == '__main__':
    socketio.run(app)
