import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    type = sa.Column(sa.String(32), nullable=False)
    nick_name = sa.Column(sa.String(40), nullable=False)
    password = sa.Column(sa.String(30), nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    __mapper_args__ = {'polymorphic_on': type}

    def __repr__(self):
        return f'<{self.type}> {self.id} {self.nick_name}'


class Masters(Users):
    __tablename__ = 'Masters'
    id = sa.Column(None, sa.ForeignKey('Users.id'), primary_key=True)
    description = sa.Column(sa.String(500))
    category = orm.relationship("Category",
                                secondary="Category_of_Masters",
                                backref="Masters")
    services = orm.relationship('Services', back_populates='Masters')
    __mapper_args__ = {'polymorphic_identity': 'Masters'}


class Clients(Users):
    __tablename__ = 'Clients'
    id = sa.Column(None, sa.ForeignKey('Users.id'), primary_key=True)
    appointments_ids = orm.relationship('Services',
                                        secondary='Appointment',
                                        backref='Clients')
    __mapper_args__ = {'polymorphic_identity': 'Clients'}
