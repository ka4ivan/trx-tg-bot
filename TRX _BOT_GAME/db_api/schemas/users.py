from datetime import datetime
from settings import db, Base


class Users_model(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger, unique=True)
    name = db.Column(db.String(300))
    user_level = db.Column(db.Integer, default=1)
    bal_usd = db.Column(db.Float, default=0)
    bal_trx = db.Column(db.Float, default=1)
    bet = db.Column(db.Float, default=1)
    join_date = db.Column(db.DateTime, default=datetime.now())
    first_referrer_id = db.Column(db.BigInteger)
    second_referrer_id = db.Column(db.BigInteger)
    third_referrer_id = db.Column(db.BigInteger)
    captcha = db.Column(db.Integer, default=0)
    mail = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    wallet_trx = db.Column(db.String(100))
    wallet_usdt = db.Column(db.String(100))
    user_language = db.Column(db.String(5), default='en')
    ban = db.Column(db.Integer, default=0)
    patron = db.Column(db.Integer, default=0)


class Users_base(Base):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger, unique=True)
    name = db.Column(db.String(300))
    user_level = db.Column(db.Integer, default=1)
    bal_usd = db.Column(db.Float, default=0)
    bal_trx = db.Column(db.Float, default=1)
    bet = db.Column(db.Float, default=1)
    join_date = db.Column(db.DateTime, default=datetime.now())
    first_referrer_id = db.Column(db.BigInteger)
    second_referrer_id = db.Column(db.BigInteger)
    third_referrer_id = db.Column(db.BigInteger)
    captcha = db.Column(db.Integer, default=0)
    mail = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    wallet_trx = db.Column(db.String(100))
    wallet_usdt = db.Column(db.String(100))
    user_language = db.Column(db.String(5), default='en')
    ban = db.Column(db.Integer, default=0)
    patron = db.Column(db.Integer, default=0)


