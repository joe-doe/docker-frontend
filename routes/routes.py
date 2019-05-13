"""
This module contains all routes for Flask application
"""
import os
from flask import render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename
from docker.errors import (
    BuildError,
    APIError,
    ContainerError,
    ImageNotFound
)


def init_routes(app, image_handler, containers_handler):
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/build-image")
    def build_image():
        dockerfile = os.path.join(app.config['UPLOAD_FOLDER'])

        try:
            image, image_build_output = image_handler.build(dockerfile)
        except BuildError:
            flash("There was an error during the build.")
            print("error_code: 1001")
            return redirect(url_for('index'))
        except APIError:
            flash("The docker API server returned error.")
            print("error_code: 1002")
            return redirect(url_for('index'))
        except TypeError as type_error:
            flash("Invalid dockerfile path")
            print("error_code: 1003")
            return redirect(url_for('index'))

        image_build_response = []
        for line in image_build_output:
            for key, value in line.items():
                image_build_response.append("{} {}\n".format(key, value))

        return render_template('build_image.html', image_build_response=image_build_response)

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

    @app.route("/select-image")
    def select_image():
        image_list = image_handler.get_image_list()
        return render_template('select_image.html', image_list=image_list)

    @app.route("/use-image", methods=['POST'])
    def use_image():
        try:
            image_id = request.form['image_id']
        except KeyError as key_error:
            flash('Wrong image id:' + str(key_error))
            return redirect(url_for('select_image'))

        try:
            image_handler.set_image(image_id)
        except ImageNotFound as image_not_found_error:
            flash("Image not found: " + image_not_found_error.explanation)
            return redirect(url_for('index'))
        except APIError as api_error:
            flash("The docker API server returned error: " + api_error.explanation)
            return redirect(url_for('index'))

        return redirect(url_for('start_container'))

    @app.route("/start-container")
    def start_container():
        image = image_handler.get_image()

        if not image:
            flash("Docker image is not available yet. Run build image first or select form list")
            return redirect(url_for('select_image'))

        try:
            containers_handler.start_new(image)
        except ContainerError as container_error:
            flash("There was an error during the new container: " + container_error.stderr)
            return redirect(url_for('index'))
        except ImageNotFound as image_not_found_error:
            flash("Image not found: " + image_not_found_error.explanation)
            return redirect(url_for('index'))
        except APIError as api_error:
            flash("The docker API server returned error: " + api_error.explanation)
            return redirect(url_for('index'))

        flash("Container started successfully")
        return redirect(url_for('index'))

    @app.route("/validate")
    def validate():
        status = containers_handler.get_containers_status()
        return render_template('validate.html', status=status)

    @app.route("/monitoring")
    def monitoring():
        return render_template('monitoring.html')

    @app.route("/logger")
    def logger():
        return render_template('logger.html')
