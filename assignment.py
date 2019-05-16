"""
Module that contains main application
and the needed initializations
"""
import sys
import os
from flask import Flask
from routes.routes import init_routes
from build_image.build_image import ImageHandler
from containers_handler.containers_handler import ContainersHandler
from monitoring.monitoring import Monitor
# EXPERIMENTAL #
# from database.database import get_db
# from flask_socketio import SocketIO
# from websocks.websocks import init_websockets

if sys.version_info < (3, 4):
    print("Sorry Python > 3.4 is needed")
    sys.exit(0)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.secret_key = os.urandom(24)

# EXPERIMENTAL #
# socketio = SocketIO(app)
# db = get_db()
# containers_handler = ContainersHandler(db)
containers_handler = ContainersHandler()

image_builder = ImageHandler()
monitor = Monitor(containers_handler)

init_routes(app, image_builder, containers_handler, monitor)

# EXPERIMENTAL #
# init_websockets(socketio, db)


if __name__ == '__main__':
    # EXPERIMENTAL #
    # socketio.run(app)
    app.run(host='0.0.0.0')
