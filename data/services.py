import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


# Таблица Услуг
class Services(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Services'  # Имя таблицы
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)  # id
    master_id = sa.Column(sa.Integer, sa.ForeignKey('Masters.id'))  # id Мастера
    name = sa.Column(sa.String)  # Название Услуги
    duration = sa.Column(sa.Time)  # Время
    price = sa.Column(sa.Integer)  # Цена
    master = orm.relationship('Masters')

    # Метод для удобного вывода
    def __repr__(self):
        return f'{self.id} - {self.name}'
