from settings import db, Base


class Bonus_model(db.Model):
    __tablename__ = "bonus"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger, unique=True)
    daily_date = db.Column(db.DateTime, default='2020-01-01 10:00:00')
    week_date = db.Column(db.DateTime, default='2020-01-01 10:00:00')


class Bonus_base(Base):
    __tablename__ = "bonus"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger, unique=True)
    daily_date = db.Column(db.DateTime, default='2020-01-01 10:00:00')
    week_date = db.Column(db.DateTime, default='2020-01-01 10:00:00')


