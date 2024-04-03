from flask import jsonify
from flask_restful import Resource, abort
from api.parser import Parser
from data import db_session
from data.users import Users


class UsersResources(Resource):
    def __init__(self):
        self.parser = Parser()
        self.parser.user_update()

    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('id', 'nick_name', 'number', 'email', 'password'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self, user_id):
        args = self.parser.parse_args()
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        user.nick_name = args['nick_name'] if args['nick_name'] is not None else user.nick_name
        user.number = args['number'] if args['number'] is not None else user.number
        user.email = args['email'] if args['email'] is not None else user.email
        user.password = args['password'] if args['password'] is not None else user.password
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResources(Resource):
    def __init__(self):
        self.parser = Parser()
        self.parser.user_update()

    def get(self):
        session = db_session.create_session()
        users = session.query(Users).all()
        return jsonify([{'users': user.to_dict(
            only=('id', 'nick_name', 'number', 'email', 'password'))} for user in users])

    def post(self):
        args = self.parser.parse_args()
        session = db_session.create_session()
        user = Users(
            nick_name=args['nick_name'],
            number=args['number'],
            email=args['email'],
            password=args['password']
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})


def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        abort(404, message=f"Users {user_id} not found")
