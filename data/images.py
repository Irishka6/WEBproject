import sqlalchemy as sa
from sqlalchemy import ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
import base64


class Images(SqlAlchemyBase, SerializerMixin):
    serialize_types = (
        (bytes, lambda x: base64.b64encode(x).decode('utf-8')),
        (str, lambda x: x)
    )
    __tablename__ = 'Images'
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.String)
    master_id = sa.Column(sa.Integer, ForeignKey('Masters.id'))
    data = sa.Column(sa.LargeBinary)
    name = sa.Column(sa.String)
    master = orm.relationship('Masters')
