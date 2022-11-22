import os
from flask import Flask

ALLOWED_EXTENSIONS = ["jpg", "png"]
PATH_TO_YOUR_FOLDER = os.getcwd()
CAMERA_ADDRESS = "rtsp://192.168.1.103/live/ch00_0"


def make_flask_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app