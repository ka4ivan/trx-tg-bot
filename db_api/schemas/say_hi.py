import datetime

from settings import db, Base


class Say_model(db.Model):
    __tablename__ = "say_hi"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)
    text_message = db.Column(db.String(1000))
    photo = db.Column(db.Boolean)
    audio = db.Column(db.Boolean)
    acces = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.now())



class Say_base(Base):
    __tablename__ = "say_hi"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)
    text_message = db.Column(db.String(1000))
    photo = db.Column(db.Boolean)
    audio = db.Column(db.Boolean)
    acces = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.now())


