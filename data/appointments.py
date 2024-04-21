import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


# Таблица Услуг
class Appointments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Appointments'  # Имя таблицы
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)  # id
    master_id = sa.Column(sa.Integer, sa.ForeignKey('Masters.id'))  # id Мастера
    client_id = sa.Column(sa.Integer, sa.ForeignKey('Clients.id'))  # id Мастера
    service_id = sa.Column(sa.Integer, sa.ForeignKey('Services.id'))
    time = sa.Column(sa.Time)  # Время
    date = sa.Column(sa.Date)  # Дата
    master = orm.relationship('Masters')
    client = orm.relationship('Clients')
    service = orm.relationship('Services')

    # Метод для удобного вывода
    def __repr__(self):
        return f'{self.id} - {self.id} id_master: {self.master_id}'
