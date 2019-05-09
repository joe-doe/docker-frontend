"""
This module contains all routes for Flask application
"""
import os
from flask import render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename


def init_routes(app):
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/build-image", methods=['GET', 'POST'])
    def build_image():
        return render_template('build_image.html')

    @app.route("/upload", methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            # Check that POST contains file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['file']

            # Check that user selected a file
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            # Check if name is Dockerfile
            if file.filename != 'Dockerfile':
                flash('Invalid file name. Should be "Dockerfile"')
                return redirect(request.url)

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully')
            return redirect(url_for('index'))

        return render_template('upload.html')

    @app.route("/start-container")
    def start_container():
        return render_template('start_container.html')

    @app.route("/monitoring")
    def monitoring():
        return render_template('monitoring.html')

    @app.route("/logger")
    def logger():
        return render_template('logger.html')
