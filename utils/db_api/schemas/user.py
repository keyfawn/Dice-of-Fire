import sqlalchemy
from utils.db_api.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String)
    all_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    win_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    darts = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    basketball = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    football = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    bowling = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    slot = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    dice = sqlalchemy.Column(sqlalchemy.Integer, default=0)
