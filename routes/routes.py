"""
This module contains all routes for Flask application
"""
import os
from flask import render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename
from docker.errors import BuildError, APIError


def init_routes(app, image_obj):
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/build-image")
    def build_image():
        dockerfile = os.path.join(app.config['UPLOAD_FOLDER'])

        try:
            image, image_build_output = image_obj.build(dockerfile)
        except BuildError as build_error:
            flash("There was an error during the build: "+build_error.msg)
            return redirect(url_for('index'))
        except APIError as api_error:
            flash("The docker API server returned error: "+api_error.explanation)
            return redirect(url_for('index'))
        except TypeError as type_error:
            flash("Invalid dockerfile path")
            print(type_error)
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

    @app.route("/start-container")
    def start_container():
        return render_template('start_container.html')

    @app.route("/monitoring")
    def monitoring():
        return render_template('monitoring.html')

    @app.route("/logger")
    def logger():
        return render_template('logger.html')
