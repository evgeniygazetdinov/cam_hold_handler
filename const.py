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


def decorator_maker_with_arguments(decorator_arg1):
    print("Я создаю декораторы! И я получил следующие аргументы:", decorator_arg1)

    def my_decorator(func):
        print(
            "Я - декоратор. И ты всё же смог передать мне эти аргументы:",
            decorator_arg1,
        )
        # Не перепутайте аргументы декораторов с аргументами функций!
        def wrapped(function_arg1, function_arg2):
            print(
                "Я - обёртка вокруг декорируемой функции.\n"
                "И я имею доступ ко всем аргументам\n"
                "\t- и декоратора: {0} {1}\n"
                "\t- и функции: {2} {3}\n"
                "Теперь я могу передать нужные аргументы дальше".format(
                    decorator_arg1, function_arg1, function_arg2
                )
            )
            return func(function_arg1, function_arg2)

        return wrapped

    return my_decorator


def my_tiny_log_decorator(func):
    def wrapper():
        print("before store")
        func()
        print("stored to db")

    return wrapper
