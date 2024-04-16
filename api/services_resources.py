from flask import jsonify
from flask_restful import Resource, abort
from api.parser import Parser
from data import db_session
from data.users import Users, Masters, Clients
from data.category import Category
from data.services import Services


# Класс для просмотра, удаления и изменения Услуг с помощью API
class ServicesResources(Resource):
    def __init__(self):
        self.parser = Parser()  # Инициализация парсера для изменения Услуги
        self.parser.service_update()

    # Получение данных Услуги по id
    def get(self, service_id):
        abort_if_service_not_found(service_id)
        session = db_session.create_session()
        service = session.query(Services).get(service_id)
        return jsonify({'service': service.to_dict(
            only=('id', 'master_id', 'name', 'description', 'price'))})

    # Удаление Услуги по id
    def delete(self, service_id):
        abort_if_service_not_found(service_id)
        session = db_session.create_session()
        service = session.query(Services).get(service_id)
        session.delete(service)
        session.commit()
        return jsonify({'success': 'OK'})

    # Изменение Услуги
    def post(self, service_id):
        args = self.parser.parse_args()
        abort_if_service_not_found(service_id)
        session = db_session.create_session()
        service = session.query(Services).get(service_id)
        service.name = args['name'] if args['name'] is not None else service.name
        service.description = args['description'] if args['description'] is not None else service.description
        service.name = args['price'] if args['price'] is not None else service.price
        session.commit()
        return jsonify({'success': 'OK'})


# Класс для получения Услуг в виде списка и добавления Услуг с помощью API
class ServicesListResources(Resource):
    def __init__(self):
        self.parser = Parser()  # Инициализация парсера для создания Услуг
        self.parser.service_add()

    # Получение массива данных Услуг
    def get(self):
        session = db_session.create_session()
        services = session.query(Services).all()
        return jsonify([{'service': user.to_dict(
            only=('id', 'master_id', 'name', 'description', 'price'))} for user in services])

    # Создание Услуги
    def post(self):
        args = self.parser.parse_args()
        session = db_session.create_session()
        user = session.query(Users).get(args['master_id'])
        if user.type != 'Masters':
            abort(404, message=f"The ID: {args['master_id']} does not belong to the master")
            return
        service = Services(
            name=args['name'],
            master_id=args['master_id'],
            description=args['description'],
            price=args['price']
        )
        session.add(service)
        session.commit()
        return jsonify({'id': service.id})


# Проверка наличия Услуги
def abort_if_service_not_found(service_id):
    session = db_session.create_session()
    service = session.query(Services).get(service_id)
    if not service:
        abort(404, message=f"Users {service_id} not found")
