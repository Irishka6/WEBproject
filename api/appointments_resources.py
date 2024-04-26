from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from data.appointments import Appointments
import datetime
from data.services import Services
from data.users import Masters
from data.db_session import create_session


# Класс для просмотра, удаления и изменения Записи с помощью API
class AppointmentsResources(Resource):
    def __init__(self):
        self.parser = RequestParser()  # Инициализация парсера для изменения Записи
        self.parser.add_argument('datetime', required=False, type=str)
        self.parser.add_argument('services', required=False, action='append', type=int)

    # Получение данных Записи по id
    def get(self, appointment_id):
        db_sess = create_session()
        abort_if_appointment_not_found(appointment_id)
        appointment = db_sess.query(Appointments).get(appointment_id)
        res = jsonify({'appointment': appointment.to_dict(
            only=('id', 'master_id', 'client_id', 'services', 'datetime'))})
        db_sess.close()
        return res

    # Удаление Записи по id
    def delete(self, appointment_id):
        db_sess = create_session()
        abort_if_appointment_not_found(appointment_id)
        appointment = db_sess.query(Appointments).get(appointment_id)
        db_sess.delete(appointment)
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}

    # Измерение Записи
    def post(self, appointment_id):
        db_sess = create_session()
        args = self.parser.parse_args()
        abort_if_appointment_not_found(appointment_id)
        appointment = db_sess.query(Appointments).get(appointment_id)
        appointment.datetime = datetime.datetime.strptime(args['datetime'], '%d.%m.%Y %H:%M') if \
            args['datetime'] is not None else appointment.datetime
        if args['services'] is not None:
            services = list(map(lambda x: db_sess.query(Services).get(x), args['services']))
            master = db_sess.query(Masters).get(appointment.master_id)
            if not all(list(map(lambda x: x in master.services, services))):
                abort(400)
            appointment.services.clear()
            appointment.services.extend(services)
        db_sess.commit()
        db_sess.close()
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
        db_sess = create_session()
        appointments = db_sess.query(Appointments).all()
        res = jsonify([{'appointment': appointment.to_dict(
            only=('id', 'master_id', 'client_id', 'services', 'datetime'))} for appointment in appointments])
        db_sess.close()
        return res

    # Создание Записи
    def post(self):
        db_sess = create_session()
        args = self.parser.parse_args()
        appointment = Appointments()
        appointment.master_id = args['master_id']
        appointment.client_id = args['client_id']
        appointment.datetime = datetime.datetime.strptime(args['datetime'], '%d.%m.%Y %H:%M')
        services = list(map(lambda x: db_sess.query(Services).get(x), args['services']))
        master = db_sess.query(Masters).get(args['master_id'])
        if not all(list(map(lambda x: x in master.services, services))):
            abort(400)
        appointment.services.extend(services)
        db_sess.add(appointment)
        db_sess.commit()
        res = {'Appointment ID': appointment.id}
        db_sess.close()
        return res


# Проверка наличия Записи
def abort_if_appointment_not_found(appointment_id):
    db_sess = create_session()
    appointment = db_sess.query(Appointments).get(appointment_id)
    if not appointment:
        abort(404, message=f"Appointment {appointment_id} not found")
    db_sess.close()
