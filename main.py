from flask import Flask, render_template, redirect, session
from flask_login import login_user, LoginManager
from flask_restful import abort, Api
from data import db_session
from api.users_resources import UsersResources, UsersListResources
from data.users import Users, Masters, Clients
from form.loginform import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'zxc_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(UsersListResources, '/api/v2/users')
api.add_resource(UsersResources, '/api/v2/users/<int:user_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


def main():
    db_session.global_init('db/db.sqlite')
    app.run()


@app.route("/", methods=['GET', 'POST'])
def index1():
    return render_template("index.html", name='')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
        # db_sess = db_session.create_session()
        # user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        # if user and form.password.data == user.password:
        #     login_user(user, remember=form.remember_me.data)
        #     return redirect('/')
        # return render_template('login.html', message='zxc', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/masters", methods=['GET', 'POST'])
def masters():
    return render_template("masters.html", name='')


if __name__ == '__main__':
    main()
