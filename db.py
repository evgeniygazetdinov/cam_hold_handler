import os
from run import app
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:////{}".format(os.path.join(project_dir, "my.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

DB = SQLAlchemy(app)
