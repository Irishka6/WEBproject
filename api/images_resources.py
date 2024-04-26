from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from data.images import Images
from data.users import Users
from data.db_session import create_session


# Класс для просмотра, удаления и изменения Изображения с помощью API
class ImagesResources(Resource):
    def __init__(self):
        self.parser = RequestParser()  # Инициализация парсера для изменения Изображения
        self.parser.add_argument('type', required=False, type=str)
        self.parser.add_argument('name', required=False, type=str)
        self.parser.add_argument('data', required=False, type=str)

    # Получение данных Изображения по id
    def get(self, image_id):
        db_sess = create_session()
        abort_if_image_not_found(image_id)
        image = db_sess.query(Images).get(image_id)
        res = jsonify({'image': image.to_dict(only=('id', 'master_id', 'type', 'name', 'data'))})
        db_sess.close()
        return res

    # Удаление Изображения по id
    def delete(self, image_id):
        db_sess = create_session()
        abort_if_image_not_found(image_id)
        image = db_sess.query(Images).get(image_id)
        db_sess.delete(image)
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}

    # Измерение Изображения
    def post(self, image_id):
        db_sess = create_session()
        args = self.parser.parse_args()
        abort_if_image_not_found(image_id)
        image = db_sess.query(Images).get(image_id)
        image.data = args['data'] if args['data'] is not None else image.data
        image.name = args['name'] if args['name'] is not None else image.name
        image.type = args['type'] if args['type'] is not None else image.type
        if args['type'] == 'avatar':
            user = db_sess.query(Users).get(image.master_id)
            avatar = list(filter(lambda x: x.type == 'avatar', user.images))
            if avatar:
                db_sess.delete(avatar[0])
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}


# Класс для получения Изображений в виде списка и добавления Услуг с помощью API
class ImagesListResources(Resource):
    def __init__(self):
        self.parser = RequestParser()  # Инициализация парсера для создания Изображения
        self.parser.add_argument('master_id', required=True, type=int)
        self.parser.add_argument('type', required=True, type=str)
        self.parser.add_argument('name', required=False, type=str)
        self.parser.add_argument('data', required=True, type=str)

    # Получение массива данных Изображений
    def get(self):
        db_sess = create_session()
        images = db_sess.query(Images).all()
        res = jsonify([{'image': image.to_dict(
            only=('id', 'master_id', 'name', 'type', 'data'))} for image in images])
        db_sess.close()
        return res

    # Создание Изображения
    def post(self):
        db_sess = create_session()
        args = self.parser.parse_args()
        img = Images()
        img.master_id = args['master_id']
        img.type = args['type']
        img.data = args['data']
        db_sess.add(img)
        img.name = args['name'] if args['name'] is not None else f'img{img.id}.jpg'
        if args['type'] == 'avatar':
            user = db_sess.query(Users).get(args['master_id'])
            avatar = list(filter(lambda x: x.type == 'avatar', user.images))
            if avatar:
                db_sess.delete(avatar[0])
        db_sess.commit()
        res = {'Image ID': img.id}
        db_sess.close()
        return res


# Проверка наличия Изображения
def abort_if_image_not_found(image_id):
    db_sess = create_session()
    image = db_sess.query(Images).get(image_id)
    if not image:
        abort(404, message=f"Image {image_id} not found")
    db_sess.close()
