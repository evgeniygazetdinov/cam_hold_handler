import os
from flask import Flask

ALLOWED_EXTENSIONS = ["jpg", "png"]
PATH_TO_YOUR_FOLDER = os.getcwd()
CAMERA_ADDRESS = "rtsp://192.168.1.103/live/ch00_0"

def add_camera_folder():
    try:
        os.mkdir("./shots")
    except OSError as error:
        pass

def make_camera_flask_app():
    app = Flask(__name__)
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:////{}".format(os.path.join(project_dir, "my.db"))
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    add_camera_folder()
    return app
