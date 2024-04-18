import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase

# # Вспомогательная таблица для записей
# association_table = sa.Table(
#     'Appointment',
#     SqlAlchemyBase.metadata,
#     sa.Column('Clients', sa.Integer, sa.ForeignKey('Clients.id')),
#     sa.Column('Services', sa.Integer, sa.ForeignKey('Services.id'))
# )


# Таблица Услуг
class Services(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Services'  # Имя таблицы
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)  # id
    master_id = sa.Column(sa.Integer, sa.ForeignKey('Masters.id'))  # id Мастера
    name = sa.Column(sa.String)  # Название Услуги
    duration = sa.Column(sa.Time)  # Время
    price = sa.Column(sa.Integer)  # Цена
    appointments = orm.relationship('Appointments', back_populates='service')
    master = orm.relationship('Masters')

    # Метод для удобного вывода
    def __repr__(self):
        return f'<{self.__tablename__}> {self.id} {self.name} id_master: {self.master_id}'
