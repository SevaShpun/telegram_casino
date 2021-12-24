import config
from sqlalchemy import create_engine, Integer, Column, Text, Table, select, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload

engine = create_engine(config.sql_login)
print('я отработал')

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, nullable=False)
    ref = Column(Integer, nullable=False)
    balance = Column(Integer, default=0)
    count_game = Column(Integer, default=0)

    def __init__(self, user_id, ref, balance, count_game=0):
        self.user_id = user_id
        self.ref = ref
        self.balance = balance
        self.count_game = count_game

    def __repr__(self):
        return "<User(user_id=%s, ref=%s, balance=%s, count_game=%s)>" % (
            self.user_id, self.ref, self.balance, self.count_game)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_new_user(user_id, ref, balance=0):
    s_user = User(user_id=user_id, ref=ref, balance=balance)
    session.add(s_user)
    session.commit()


def get_all_users():
    s = session.query(User).all()
    return [(i.id, i.user_id, i.ref, i.balance, i.count_game) for i in s]


def exist_user(user_id):
    s = session.query(User).filter_by(user_id=user_id).all()
    return bool(len(s))


def count_refs(user_id):
    s = session.query(User).filter_by(ref=user_id).all()
    return len(s)


def get_user_info(user_id):
    if not exist_user(user_id):
        return [0, 0, 0]
    user = session.query(User).filter_by(user_id=user_id).first()
    return [user.balance, count_refs(user_id), user.count_game]


def update_balance(user_id, count):
    s = session.query(User).filter_by(user_id=user_id).first()
    count_balance = s.balance
    u = update(User).where(User.user_id == user_id).values(balance=count_balance + count).\
        execution_options(synchronize_session="fetch")
    session.execute(u)
    session.commit()
    return True


def update_count_game(user_id):
    s = session.query(User).filter_by(user_id=user_id).first()
    count_game = s.count_game
    u = update(User).where(User.user_id == user_id).values(count_game=count_game + 1).\
        execution_options(synchronize_session="fetch")
    session.execute(u)
    session.commit()
    return True


def get_user_balance(user_id):
    s = session.query(User).filter_by(user_id=user_id).first()
    return s.balance
