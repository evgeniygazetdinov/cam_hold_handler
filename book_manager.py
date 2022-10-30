from db import DB 


class Book(DB.Model):
    title = DB.Column(DB.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)