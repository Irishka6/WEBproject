import sqlalchemy as sa
from sqlalchemy import ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Images(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Images'
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.String)
    master_id = sa.Column(sa.Integer, ForeignKey('Masters.id'))
    data = sa.Column(sa.BLOB(length=16777215))
    name = sa.Column(sa.String)
    master = orm.relationship('Masters')
