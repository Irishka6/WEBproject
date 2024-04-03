from flask_restful.reqparse import RequestParser


class Parser(RequestParser):
    def user_add(self):
        self.add_argument('nick_name', required=True, type=str)
        self.add_argument('number', required=True, type=str)
        self.add_argument('email', required=True, type=str)
        self.add_argument('password', required=True, type=str)

    def user_update(self):
        self.add_argument('nick_name', required=False, type=str)
        self.add_argument('number', required=False, type=str)
        self.add_argument('email', required=False, type=str)
        self.add_argument('password', required=False, type=str)
