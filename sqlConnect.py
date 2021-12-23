import config
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Integer, Column, Text, Table, select, update

engine = create_engine(config.sql_login)
conn = engine.connect()
print('я отработал')

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('user_id', Integer(), nullable=False),
              Column('ref', Integer(), nullable=False),
              Column('balance', Integer(), default=0),
              Column('count_game', Integer(), default=0))


def add_new_user(user_id, ref, balance=0):
    ins = users.insert().values(
        user_id=user_id,
        ref=ref,
        balance=balance
    )
    conn.execute(ins)


def get_all_users():
    s = select([users])
    return conn.execute(s).fetchall()


def exist_user(user_id):
    s = select([users]).where(users.c.user_id == user_id)
    return bool(len(conn.execute(s).fetchall()))


def count_refs(user_id):
    s = select([users]).where(users.c.ref == user_id)
    return len(conn.execute(s).fetchall())


def get_user_info(user_id):
    if not exist_user(user_id):
        return [0, 0, 0]
    user_tmp = select([users]).where(users.c.user_id == user_id)
    user = conn.execute(user_tmp).fetchall()[0]
    return [user[3], count_refs(user_id), user[4]]


def update_balance(user_id, count):
    s = select([users]).where(users.c.user_id == user_id)
    count_balance = conn.execute(s).fetchall()[0][3]
    u = (update(users).where(users.c.user_id == user_id).values(balance=count_balance + count))
    conn.execute(u)

# metadata.create_all(engine)
