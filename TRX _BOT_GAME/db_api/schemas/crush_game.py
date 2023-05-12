from settings import db, Base


class Crush_model(db.Model):
    __tablename__ = "crush_game"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)
    num_game = db.Column(db.Float)
    coef = db.Column(db.Float)
    stop = db.Column(db.Boolean)



class Crush_base(Base):
    __tablename__ = "crush_game"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)
    num_game = db.Column(db.Float)
    coef = db.Column(db.Float)
    stop = db.Column(db.Boolean)


