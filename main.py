import string
from random import choice

from flask import Flask, render_template, redirect, session, request
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from flask_restful import abort, Api
from data import db_session
from api.users_resources import UsersResources, UsersListResources
from data.users import Users, Masters, Clients
from form.loginform import LoginForm
from form.registr import RegisterForm
from form.regmast import RegisterFormMaster
from form.dobyslyg import DobyslForm
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zxc_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(UsersListResources, '/api/v2/users')
api.add_resource(UsersResources, '/api/v2/users/<int:user_id>')
app.secret_key = ''.join(choice(string.ascii_letters) for _ in range(30))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).filter_by(id=user_id).first()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init('db/db.sqlite')
    app.run()


@app.route("/", methods=['GET', 'POST'])
def index1():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user.password == form.password.data:
           login_user(user)
           return redirect("/")
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/masters", methods=['GET', 'POST'])
def masters():
    return render_template("masters.html", name='')


@app.route("/registrate", methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("registrate.html", name='', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == str(form.email.data)).first():
            return render_template("registrate.html", name='', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        if form.use.data == 'Мастер':
            db_sess = db_session.create_session()
            print(form.use.data)
            user = Masters(nick_name=form.name.data,
                         password=form.password.data,
                         email=form.email.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect("/login")
        else:
            db_sess = db_session.create_session()
            print(form.use.data)
            user = Clients(nick_name=form.name.data,
                           password=form.password.data,
                           email=form.email.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect("/login")
    return render_template("registrate.html", name='', form=form)


@app.route("/mast/<int:id>", methods=["GET", "POST"])
def move_forward(id):
    form = RegisterFormMaster()
    # здесь добавить вставку уже имеющихся значенй взятых из БД по айди мастера
    if form.validate_on_submit():
        # здесь изменить в БД нововведенные данные форма называется regmast.py in form
        return redirect("/login")
    return render_template("regmas.html", name='', form=form)

@app.route("/stranichca") # надо добавить /int:id как только будешь связывать с БД мастеров
def stranichka():
    im = Image.open('static/img/par.jpg')# загружается аватарка сохраненая d БД
    pi = im.load()
    r, g, b, total = 0, 0, 0, 0
    x, y = im.size
    for i in range(x):
        for j in range(y):
            total += 1
            r += pi[i, j][0]
            g += pi[i, j][1]
            b += pi[i, j][2]
    rgb = str((r // total, g // total, b // total))
    # поле аватар заменить путем к фото которое сохраняется в папку при просмотреа после удаляеется
    # тут надо достать все данные по мастеру прям все и загрузить в render_template
    return render_template("stranighka.html", name='', foto=rgb, prais='Маникюр-650', sety='сылки', avatar="static/img/par.jpg", ysluga=[["Маникюр", "1600", "1час 30 мин"], ["Маникюр", "1600", "1час 30 мин"]])

@app.route("/zapis")
def zapis():
    pass

@app.route("/dobysl")
def dobysl():
    form = DobyslForm()
    if form.validate_on_submit():
        #  тут нужно сохранить то что введенно в форме в БД
        return redirect("/stranichca")
    return render_template("dobysl.html", form=form)

if __name__ == '__main__':
    main()
