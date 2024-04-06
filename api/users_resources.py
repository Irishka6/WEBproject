from flask import jsonify
from flask_restful import Resource, abort
from api.parser import Parser
from data import db_session
from data.users import Users, Masters, Clients
from data.category import Category, create_category


class UsersResources(Resource):
    def __init__(self):
        self.parser = Parser()
        self.parser.user_update()

    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('id', 'type', 'nick_name', 'number', 'email', 'password'))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self, user_id):
        args = self.parser.parse_args()
        abort_if_users_not_found(user_id)
        abort_if_type_invalid(args['type'])
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        user.nick_name = args['nick_name'] if args['nick_name'] is not None else user.nick_name
        user.name = args['name'] if args['name'] is not None else user.name
        user.surname = args['surname'] if args['surname'] is not None else user.surname
        user.number = args['number'] if args['number'] is not None else user.number
        user.email = args['email'] if args['email'] is not None else user.email
        user.password = args['password'] if args['password'] is not None else user.password
        if user.type == 'Masters':
            user.description = args['description'] if args['description'] is not None else user.description
            if args['category'] is not None:
                c = session.query(Category).filter(Category.id==args['category']).first()
                if c is None:
                    create_category()
                    c = session.query(Category).filter(Category.id == args['category']).first()
                user.category[0] = c
        elif user.type == 'Clients':
            user.appointments_ids = args['appointments_ids'] \
                if args['appointments_ids'] is not None else user.appointments_ids
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResources(Resource):
    def __init__(self):
        self.parser = Parser()
        self.parser.user_add()

    def get(self):
        session = db_session.create_session()
        users = session.query(Users).all()
        return jsonify([{'users': user.to_dict(
            only=('id', 'type', 'nick_name', 'number', 'email', 'password'))} for user in users])

    def post(self):
        args = self.parser.parse_args()
        abort_if_type_invalid(args['type'])
        session = db_session.create_session()
        if args['type'] == 'Masters':
            user = Masters(
                nick_name=args['nick_name'],
                name=args['name'],
                surname=args['surname'],
                number=args['number'],
                email=args['email'],
                password=args['password'],
                description=args['description']
            )
            c = session.query(Category).filter(Category.id == args['category']).first()
            if c is None:
                create_category()
                c = session.query(Category).filter(Category.id == args['category']).first()
            user.category.append(c)
        elif args['type'] == 'Clients':
            user = Clients(
                nick_name=args['nick_name'],
                name=args['name'],
                surname=args['surname'],
                number=args['number'],
                email=args['email'],
                password=args['password'],
                appointments_ids=args['appointments_ids']
            )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})


def abort_if_type_invalid(type):
    if type not in ['Masters', 'Clients']:
        abort(404, message=f'Invalid type {type}: using "Masters" or "Clients"')


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        abort(404, message=f"Users {user_id} not found")
