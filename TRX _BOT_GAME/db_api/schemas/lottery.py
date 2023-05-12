from settings import db, Base


class Lottery_model(db.Model):
    __tablename__ = "lottery"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)



class Lottery_base(Base):
    __tablename__ = "lottery"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.BigInteger)



