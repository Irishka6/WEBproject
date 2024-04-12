import sqlalchemy as sa
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    type = sa.Column(sa.String, nullable=False)
    nick_name = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    __mapper_args__ = {'polymorphic_on': type}

    def __repr__(self):
        return f'<{self.type}> {self.id} {self.nick_name}'



class Masters(Users):
    __tablename__ = 'Masters'
    id = sa.Column(None, sa.ForeignKey('Users.id'), primary_key=True)
    description = sa.Column(sa.String(500))
    category = orm.relationship("Category",
                                secondary="category_of_masters",
                                backref="Masters")
    __mapper_args__ = {'polymorphic_identity': 'Masters'}


class Clients(Users):
    __tablename__ = 'Clients'
    id = sa.Column(None, sa.ForeignKey('Users.id'), primary_key=True)
    appointments_ids = sa.Column(sa.String(500))
    __mapper_args__ = {'polymorphic_identity': 'Clients'}
