from settings import db, Base


class Promo_model(db.Model):
    __tablename__ = "promo_code"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)
    promo_code = db.Column(db.String(10))
    c_promo_code = db.Column(db.Integer)


class Promo_base(Base):
    __tablename__ = "promo_code"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)
    promo_code = db.Column(db.String(10))
    c_promo_code = db.Column(db.Integer)


