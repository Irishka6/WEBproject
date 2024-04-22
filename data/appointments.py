import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from data.services import Services
from data.users import Users


association_table = sa.Table(
    'Services_to_Appointment',
    SqlAlchemyBase.metadata,
    sa.Column('Services', sa.Integer, sa.ForeignKey('Services.id')),
    sa.Column('Appointment', sa.Integer, sa.ForeignKey('Appointments.id'))
)


# Таблица Услуг
class Appointments(SqlAlchemyBase, SerializerMixin):
    serialize_types = (
        (Services, lambda x: {"id": x.id, "name": x.name, "duration": str(x.duration), "price": x.price}),
        (dict, lambda x: x)
    )
    __tablename__ = 'Appointments'  # Имя таблицы
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)  # id
    master_id = sa.Column(sa.Integer, sa.ForeignKey('Masters.id'))  # id Мастера
    client_id = sa.Column(sa.Integer, sa.ForeignKey('Clients.id'))  # id Мастера
    services = orm.relationship('Services', secondary='Services_to_Appointment', backref='appointments')
    datetime = sa.Column(sa.DateTime)  # Дата и Время
    master = orm.relationship('Masters')
    client = orm.relationship('Clients')

    # Метод для удобного вывода
    def __repr__(self):
        return f'{self.id} - {self.id} id_master: {self.master_id}'
