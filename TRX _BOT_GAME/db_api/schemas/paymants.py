from settings import db, Base


class Paymants_model(db.Model):
    __tablename__ = "paymants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)
    add_usd = db.Column(db.Integer)
    add_trx = db.Column(db.Integer)
    del_trx = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    adress = db.Column(db.String(100))
    acces = db.Column(db.Integer)


class Paymants_base(Base):
    __tablename__ = "paymants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)
    add_usd = db.Column(db.Integer)
    add_trx = db.Column(db.Integer)
    del_trx = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    adress = db.Column(db.String(100))
    acces = db.Column(db.Integer)


