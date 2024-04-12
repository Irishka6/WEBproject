import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


association_table = sa.Table(
    'Appointment',
    SqlAlchemyBase.metadata,
    sa.Column('Clients', sa.Integer, sa.ForeignKey('Clients.id')),
    sa.Column('Services', sa.Integer, sa.ForeignKey('Services.id'))
)


class Services(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Services'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    master = sa.Column(sa.Integer, sa.ForeignKey('Masters.id'))
    name = sa.Column(sa.String)
    description = sa.Column(sa.String)
    price = sa.Column(sa.Integer)
    m = orm.relationship('Masters')

    def __repr__(self):
        return f'<{self.__tablename__}> {self.id} {self.name} id_master: {self.master}'
