from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from data.db_session import db_sess
from data.users import Users, Masters, Clients
from data.category import Category


# Класс для просмотра, удаления и изменения пользователя с помощью API
class UsersResources(Resource):
    def __init__(self):
        self.parser = RequestParser()  # Инициализация парсера для изменения пользователя
        self.parser.add_argument('nick_name', required=False, type=str)
        self.parser.add_argument('email', required=False, type=str)
        self.parser.add_argument('password', required=False, type=str)
        self.parser.add_argument('description', required=False, type=str)
        self.parser.add_argument('category', required=False, type=str)
        self.parser.add_argument('address', required=False, type=str)
        self.parser.add_argument('social', required=False, type=str)

    # Получение данных пользователя по id
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        user = db_sess.query(Users).get(user_id)
        if user.type == 'Clients':
            return jsonify({'users': user.to_dict(
                only=('id', 'type', 'nick_name', 'email', 'hashed_password', 'appointments'))})
        elif user.type == 'Masters':
            return jsonify({'users': user.to_dict(
                only=('id', 'type', 'nick_name', 'email', 'hashed_password', 'description', 'category', 'address',
                      'social', 'images', 'registrate', 'services', 'appointments'))})

    # Удаление пользователя по id
    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        user = db_sess.query(Users).get(user_id)
        if user.type == 'Masters':
            for img in user.images:
                db_sess.delete(img)
            for ser in user.services:
                db_sess.delete(ser)
        for appointment in user.appointments:
            db_sess.delete(appointment)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    # Изменение пользователя
    def post(self, user_id):
        args = self.parser.parse_args()
        abort_if_users_not_found(user_id)
        user = db_sess.query(Users).get(user_id)
        user.nick_name = args['nick_name'] if args['nick_name'] is not None else user.nick_name
        user.email = args['email'] if args['email'] is not None else user.email
        if args['password'] is not None:
            user.set_password(args['password'])
        if user.type == 'Masters':
            user.description = args['description'] if args['description'] is not None else user.description
            user.address = args['address'] if args['address'] is not None else user.address
            user.social = args['social'] if args['social'] is not None else user.social
            if args['category'] is not None:
                c = db_sess.query(Category).filter(Category.name==args['category']).first()
                user.category[0] = c
        db_sess.commit()
        return jsonify({'success': 'OK'})


# Класс для получения пользователя в виде списка и добавления Услуг с помощью API
class UsersListResources(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('nick_name', required=True, type=str)
        self.parser.add_argument('email', required=True, type=str)
        self.parser.add_argument('password', required=True, type=str)
        self.parser.add_argument('type', required=True, type=str)
        self.parser.add_argument('description', required=False, type=str)
        self.parser.add_argument('category', required=False, type=str)
        self.parser.add_argument('address', required=False, type=str)
        self.parser.add_argument('social', required=False, type=str)

    # Получение массива данных пользователей
    def get(self):
        users = db_sess.query(Users).all()
        return jsonify([{'user': user.to_dict(
            only=('id', 'type', 'nick_name', 'email', 'hashed_password', 'appointments'))} if user.type == 'Clients' else
            {'user': user.to_dict(only=('id', 'type', 'nick_name', 'email', 'hashed_password',
                                        'description', 'category', 'services', 'address', 'social', 'images',
                                        'registrate', 'appointments'))}
            for user in users])

    # Создание пользователя
    def post(self):
        args = self.parser.parse_args()
        abort_if_type_invalid(args['type'])
        abort_if_invalid_data(args['type'], args)
        if args['type'] == 'Masters':
            user = Masters(
                description=args['description'],
                address=args['address'],
                social=args['social'],
                registrate=True
            )
            c = db_sess.query(Category).filter(Category.name == args['category']).first()
            user.category.append(c)
        elif args['type'] == 'Clients':
            user = Clients()
        user.nick_name = args['nick_name']
        user.email = args['email']
        user.set_password(args['password'])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'User ID': user.id})


def abort_if_invalid_data(type, args):
    if type == 'Masters':
        list_args = [args['description'], args['address'], args['social'], args['category']]
        if not all(list_args):
            abort(400, message=f"Invalid data for creating a user.")


# Проверка валидности типа
def abort_if_type_invalid(type):
    if type not in ['Masters', 'Clients']:
        abort(400, message=f"Invalid type {type}: using 'Masters' or 'Clients'")


# Проверка наличия пользователя
def abort_if_users_not_found(user_id):
    user = db_sess.query(Users).get(user_id)
    if not user:
        abort(404, message=f"Users {user_id} not found")
