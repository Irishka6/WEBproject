from flask_restful.reqparse import RequestParser


# Парсер для отслеживания аргументов
class Parser(RequestParser):
    # Аргументы для создания пользователя
    def user_add(self):
        self.add_argument('nick_name', required=True, type=str)
        self.add_argument('email', required=True, type=str)
        self.add_argument('password', required=True, type=str)
        self.add_argument('type', required=True, type=str)
        self.add_argument('description', required=False, type=str)
        self.add_argument('category', required=False, type=str)
        self.add_argument('address', required=False, type=str)
        self.add_argument('social', required=False, type=str)

    # Аргументы для редактирования пользователя
    def user_update(self):
        self.add_argument('nick_name', required=False, type=str)
        self.add_argument('email', required=False, type=str)
        self.add_argument('password', required=False, type=str)
        self.add_argument('description', required=False, type=str)
        self.add_argument('category', required=False, type=str)
        self.add_argument('address', required=False, type=str)
        self.add_argument('social', required=False, type=str)

    def service_add(self):
        self.add_argument('name', required=True, type=str)
        self.add_argument('master_id', required=True, type=int)
        self.add_argument('description', required=False, type=str)
        self.add_argument('price', required=True, type=int)

    def service_update(self):
        self.add_argument('name', required=False, type=str)
        self.add_argument('description', required=False, type=str)
        self.add_argument('price', required=False, type=int)
