from flask_restful.reqparse import RequestParser


class Parser(RequestParser):
    def user_add(self):
        self.add_argument('nick_name', required=True, type=str)
        self.add_argument('name', required=True, type=str)
        self.add_argument('surname', required=True, type=str)
        self.add_argument('number', required=True, type=str)
        self.add_argument('email', required=True, type=str)
        self.add_argument('password', required=True, type=str)
        self.add_argument('type', required=True, type=str)
        self.add_argument('description', required=False, type=str)
        self.add_argument('appointments_ids', required=False, type=str)
        self.add_argument('category', required=False, type=str)

    def user_update(self):
        self.add_argument('nick_name', required=False, type=str)
        self.add_argument('name', required=False, type=str)
        self.add_argument('surname', required=False, type=str)
        self.add_argument('number', required=False, type=str)
        self.add_argument('email', required=False, type=str)
        self.add_argument('password', required=False, type=str)
        self.add_argument('description', required=False, type=str)
        self.add_argument('appointments_ids', required=False, type=str)
        self.add_argument('category', required=False, type=str)
