"""
This module contains all routes for Flask application
"""
from flask import render_template, url_for


def init_routes(app):
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/build-image")
    def build_image():
        return render_template('build_image.html')

    @app.route("/start-container")
    def start_container():
        return render_template('start_container.html')

    @app.route("/monitoring")
    def monitoring():
        return render_template('monitoring.html')

    @app.route("/logger")
    def logger():
        return render_template('logger.html')
