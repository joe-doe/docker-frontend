"""


"""
import os
from flask import Flask
from routes.routes import init_routes
from build_image.build_image import ImageHandler
from start_container.start_container import ContainersHandler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.secret_key = os.urandom(24)

image_builder = ImageHandler()
containers_handler = ContainersHandler()

init_routes(app, image_builder, containers_handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
