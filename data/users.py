import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_utils import PhoneNumberType, PhoneNumber
from flask_login import UserMixin
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    serialize_types = (
        (PhoneNumber, lambda x: x.international),
        (str, lambda x: x)
    )
    __tablename__ = 'Users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nick_name = sa.Column(sa.String(40))
    password = sa.Column(sa.String(30))
    email = sa.Column(sa.String, unique=True)
    number = sa.Column(PhoneNumberType('RU'), unique=True)
