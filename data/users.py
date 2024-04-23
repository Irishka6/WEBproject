import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.category import Category
from data.images import Images
from data.services import Services
from data.appointments import Appointments

from data.db_session import SqlAlchemyBase


# Основная таблица пользователя
# Тут будут храниться основные данные о пользователе (ник, почта, хэш пароля, тип пользователя)
class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Users'  # Имя таблицы
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)  # id пользователя

    type = sa.Column(sa.String(32), nullable=False)  # тип пользователя, может быть либо Masters, либо Clients/
    nick_name = sa.Column(sa.String(40), nullable=False)  # ник пользователя
    hashed_password = sa.Column(sa.String(500), nullable=False)  # хэш пароля пользователя
    email = sa.Column(sa.String(50), unique=True, nullable=False)  # почта пользователя
    __mapper_args__ = {'polymorphic_on': type}  # для корректного наследования классов

    # Метод для удобного вывода
    def __repr__(self):
        return f'<{self.type}> {self.id} {self.nick_name} {self.email} {self.hashed_password}'

    # Метод для установки пароля
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # Метод для проверки того, что переданный пароль (password) идентичен хэшированному паролю
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


# Таблица Мастеров
class Masters(Users):
    # Сериализация Категорий для корректного отображения в API
    serialize_types = (
        (Category, lambda x: x.name),
        (str, lambda x: x),
        (Services, lambda x: {"id": x.id, "name": x.name, "duration": str(x.duration), "price": x.price}),
        (Images, lambda x: {'id': x.id, 'master_id': x.master_id, 'name': x.name, 'type': x.type}),
        (dict, lambda x: x),
        (Appointments, lambda x: x.to_dict(only=('datetime', 'client_id', 'services'))),
        (dict, lambda x: x)
    )

    __tablename__ = 'Masters'  # Имя таблицы
    id = sa.Column(None, sa.ForeignKey('Users.id'), primary_key=True)  # id Мастера
    description = sa.Column(sa.String(500))  # описание Мастера
    address = sa.Column(sa.String(150))  # Адрес Мастера
    social = sa.Column(sa.String(250))
    registrate = sa.Column(sa.Boolean, default=False)
    category = orm.relationship("Category",
                                secondary="Category_of_Masters",
                                backref="Masters")  # Категории Мастера
    services = orm.relationship('Services', back_populates='master')  # Услуги Мастера
    images = orm.relationship('Images', back_populates='master')
    appointments = orm.relationship('Appointments', back_populates='master')
    __mapper_args__ = {'polymorphic_identity': 'Masters'}  # для наследования от класса Users

    def __repr__(self):
        return f'{self.id} - {self.nick_name} {self.category}'


# Таблица Клиентов
class Clients(Users):
    serialize_types = (
        (Appointments, lambda x: x.to_dict(only=('datetime', 'master_id', 'services'))),
        (dict, lambda x: x)
    )
    __tablename__ = 'Clients'  # Имя таблицы
    id = sa.Column(None, sa.ForeignKey('Users.id'), primary_key=True)  # id Клиента
    appointments = orm.relationship('Appointments', back_populates='client')  # Записи на приём к Мастерам
    __mapper_args__ = {'polymorphic_identity': 'Clients'}  # для наследования от класса Users