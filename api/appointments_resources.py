from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from data import db_session
from data.appointments import Appointments
import datetime

from data.services import Services
from data.users import Masters


# Класс для просмотра, удаления и изменения Записи с помощью API
class AppointmentsResources(Resource):
    def __init__(self):
        self.parser = RequestParser()  # Инициализация парсера для изменения Записи
        self.parser.add_argument('datetime', required=False, type=str)
        self.parser.add_argument('services', required=False, action='append', type=int)

    # Получение данных Записи по id
    def get(self, appointment_id):
        abort_if_appointment_not_found(appointment_id)
        session = db_session.create_session()
        appointment = session.query(Appointments).get(appointment_id)
        return jsonify({'appointment': appointment.to_dict(
            only=('id', 'master_id', 'client_id', 'services', 'datetime'))})

    # Удаление Записи по id
    def delete(self, appointment_id):
        abort_if_appointment_not_found(appointment_id)
        session = db_session.create_session()
        appointment = session.query(Appointments).get(appointment_id)
        session.delete(appointment)
        session.commit()
        return {'success': 'OK'}

    # Измерение Записи
    def post(self, appointment_id):
        args = self.parser.parse_args()
        abort_if_appointment_not_found(appointment_id)
        session = db_session.create_session()
        appointment = session.query(Appointments).get(appointment_id)
        appointment.datetime = datetime.datetime.strptime(args['datetime'], '%d.%m.%Y %H:%M') if \
            args['datetime'] is not None else appointment.datetime
        if args['services'] is not None:
            services = list(map(lambda x: session.query(Services).get(x), args['services']))
            master = session.query(Masters).get(appointment.master_id)
            if not all(list(map(lambda x: x in master.services, services))):
                abort(400)
            appointment.services.clear()
            appointment.services.extend(services)
        session.commit()
        return {'success': 'OK'}


# Класс для получения Изображений в виде списка и добавления Записей с помощью API
class AppointmentsListResources(Resource):
    def __init__(self):
        self.parser = RequestParser()  # Инициализация парсера для создания Записи
        self.parser.add_argument('master_id', required=True, type=int)
        self.parser.add_argument('client_id', required=True, type=str)
        self.parser.add_argument('datetime', required=True, type=str)
        self.parser.add_argument('services', required=True, action='append', type=int)

    # Получение массива данных Записей
    def get(self):
        session = db_session.create_session()
        appointments = session.query(Appointments).all()
        return jsonify([{'appointment': appointment.to_dict(
            only=('id', 'master_id', 'client_id', 'services', 'datetime'))} for appointment in appointments])

    # Создание Записи
    def post(self):
        args = self.parser.parse_args()
        session = db_session.create_session()
        appointment = Appointments()
        appointment.master_id = args['master_id']
        appointment.client_id = args['client_id']
        appointment.datetime = datetime.datetime.strptime(args['datetime'], '%d.%m.%Y %H:%M')
        services = list(map(lambda x: session.query(Services).get(x), args['services']))
        master = session.query(Masters).get(args['master_id'])
        if not all(list(map(lambda x: x in master.services, services))):
            abort(400)
        appointment.services.extend(services)
        session.add(appointment)
        session.commit()
        return {'Appointment ID': appointment.id}


# Проверка наличия Записи
def abort_if_appointment_not_found(appointment_id):
    session = db_session.create_session()
    appointment = session.query(Appointments).get(appointment_id)
    if not appointment:
        abort(404, message=f"Appointment {appointment_id} not found")
