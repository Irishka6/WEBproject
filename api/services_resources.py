from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from data.db_session import db_sess
from data.users import Users
from data.services import Services
import datetime


# Класс для просмотра, удаления и изменения Услуг с помощью API
class ServicesResources(Resource):
    def __init__(self):
        self.parser = RequestParser()  # Инициализация парсера для изменения Услуги
        self.parser.add_argument('name', required=False, type=str)
        self.parser.add_argument('duration', required=False, type=str)
        self.parser.add_argument('price', required=False, type=int)

    # Получение данных Услуги по id
    def get(self, service_id):
        abort_if_service_not_found(service_id)
        service = db_sess.query(Services).get(service_id)
        return jsonify({'service': service.to_dict(
            only=('id', 'master_id', 'name', 'duration', 'price'))})

    # Удаление Услуги по id
    def delete(self, service_id):
        abort_if_service_not_found(service_id)
        service = db_sess.query(Services).get(service_id)
        db_sess.delete(service)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    # Изменение Услуги
    def post(self, service_id):
        args = self.parser.parse_args()
        abort_if_service_not_found(service_id)
        service = db_sess.query(Services).get(service_id)
        service.name = args['name'] if args['name'] is not None else service.name
        service.duration = datetime.datetime.strptime(args['duration'], '%H:%M').time() if args['duration'] is not None else service.duration
        service.name = args['price'] if args['price'] is not None else service.price
        db_sess.commit()
        return jsonify({'success': 'OK'})


# Класс для получения Услуг в виде списка и добавления Услуг с помощью API
class ServicesListResources(Resource):
    def __init__(self):
        self.parser = RequestParser()  # Инициализация парсера для создания Услуг
        self.parser.add_argument('name', required=True, type=str)
        self.parser.add_argument('master_id', required=True, type=int)
        self.parser.add_argument('duration', required=False, type=str)
        self.parser.add_argument('price', required=True, type=int)

    # Получение массива данных Услуг
    def get(self):
        services = db_sess.query(Services).all()
        return jsonify([{'service': service.to_dict(
            only=('id', 'master_id', 'name', 'duration', 'price'))} for service in services])

    # Создание Услуги
    def post(self):
        args = self.parser.parse_args()
        user = db_sess.query(Users).get(args['master_id'])
        if user.type != 'Masters':
            abort(400, message=f"The ID: {args['master_id']} does not belong to the master")
        service = Services(
            name=args['name'],
            master_id=args['master_id'],
            duration=datetime.datetime.strptime(args['duration'], '%H:%M').time(),
            price=args['price']
        )
        db_sess.add(service)
        db_sess.commit()
        return jsonify({'Service ID': service.id})


# Проверка наличия Услуги
def abort_if_service_not_found(service_id):
    service = db_sess.query(Services).get(service_id)
    if not service:
        abort(404, message=f"Service {service_id} not found")
