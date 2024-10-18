from settings import db, Base


class Stats_model(db.Model):
    __tablename__ = "stats"

    all_acc = db.Column(db.Integer, primary_key=True)
    day_acc = db.Column(db.Integer)
    active_acc = db.Column(db.Integer)
    pay_trx = db.Column(db.Float)


class Stats_base(Base):
    __tablename__ = "stats"

    all_acc = db.Column(db.Integer, primary_key=True)
    day_acc = db.Column(db.Integer)
    active_acc = db.Column(db.Integer)
    pay_trx = db.Column(db.Float)

