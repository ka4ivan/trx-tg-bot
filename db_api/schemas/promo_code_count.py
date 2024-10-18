from settings import db, Base


class Promo_count_model(db.Model):
    __tablename__ = "promo_code_count"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    promo_code = db.Column(db.String(10))
    count_promo_code = db.Column(db.Integer)


class Promo_count_base(Base):
    __tablename__ = "promo_code_count"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    promo_code = db.Column(db.String(10))
    count_promo_code = db.Column(db.Integer)


