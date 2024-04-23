import base64
import string
from random import choice
from flask import Flask, render_template, redirect, send_file
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from flask_restful import abort, Api
from data.db_session import db_sess
from api.users_resources import UsersResources, UsersListResources
from api.services_resources import ServicesResources, ServicesListResources
from api.images_resources import ImagesResources, ImagesListResources
from api.appointments_resources import AppointmentsResources, AppointmentsListResources
from data.category import Category, create_category
from data.images import Images
from data.users import Users, Masters, Clients
from data.services import Services
from form.loginform import LoginForm
from form.registr import RegisterForm
from form.regmast import RegisterFormMaster
from form.dobyslyg import DobyslForm
from PIL import Image
from io import BytesIO
import asyncio


class App(Flask):
    def __init__(self, import_name: str):
        super().__init__(import_name)
        self.config['SECRET_KEY'] = 'zxc_secret_key'
        self.db_sess = db_sess
        self.api = Api(self)
        self.login_manager = LoginManager()
        self.login_manager.init_app(self)
        self.api.add_resource(UsersListResources, '/api/v2/users')
        self.api.add_resource(UsersResources, '/api/v2/users/<int:user_id>')
        self.api.add_resource(ServicesListResources, '/api/v2/services')
        self.api.add_resource(ServicesResources, '/api/v2/services/<int:service_id>')
        self.api.add_resource(ImagesResources, '/api/v2/images/<int:image_id>')
        self.api.add_resource(ImagesListResources, '/api/v2/images')
        self.api.add_resource(AppointmentsResources, '/api/v2/appointments/<int:appointment_id>')
        self.api.add_resource(AppointmentsListResources, '/api/v2/appointments')
        self.secret_key = ''.join(choice(string.ascii_letters) for _ in range(30))
        self.check_category()  # костыль
        self.check_photo()

    # костыль
    def check_category(self):
        categories = self.db_sess.query(Category).all()
        if len(categories) == 0:
            create_category()

    def check_photo(self):
        photos = self.db_sess.query(Images).all()
        if len(list(filter(lambda x: x.type == 'default', photos))) == 0:
            with open('static/img/default.jpg', 'rb') as f:
                d = base64.b64encode(f.read())
            img = Images(name='default.jpg', data=d, type='default')
            self.db_sess.add(img)
            self.db_sess.commit()


app = App(__name__)


@app.login_manager.user_loader
def load_user(user_id):
    return app.db_sess.query(Users).filter_by(id=user_id).first()


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route("/", methods=['GET', 'POST'])
def index1():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = app.db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect("/")
            return render_template('login.html', title='Авторизация', message='Неверный пароль', form=form)
        return render_template('login.html', title='Авторизация', message='Такого пользователя нет', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/masters/<typ>")
def masters(typ):
    users = app.db_sess.query(Masters).all()
    user = []
    for i in users:
        print(i.category.__repr__()[1:len(i.category.__repr__()) - 1], typ)
        if i.category.__repr__()[1:len(i.category.__repr__()) - 1] == typ:
            user.append(i)
    ids_avatars = asyncio.run(main_get_avatar(users))
    return render_template("masters.html", users=user, avatars=ids_avatars)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("registration.html", name='', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if app.db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template("registration.html", name='', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        if form.use.data == 'Мастер':
            user = Masters()
        else:
            user = Clients()
        user.nick_name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        app.db_sess.add(user)
        app.db_sess.commit()
        login_user(user)
        if form.use.data == 'Мастер':
            return redirect(f"/registration_master/{user.id}")
        return redirect('/')
    return render_template("registration.html", form=form)


@app.route("/registration_master/<int:master_id>", methods=["GET", "POST"])
@login_required
def registration_master(master_id):
    master = app.db_sess.query(Masters).get(master_id)
    if current_user.id == master.id and master.registrate is False:
        form = RegisterFormMaster()
        if form.validate_on_submit():
            master.category.append(app.db_sess.query(Category).filter(Category.name==form.category.data).first())
            master.address = form.address.data
            master.social = form.telegram.data
            master.description = form.description.data
            master.registrate = True
            img = Images(type='avatar', master_id=master.id, data=base64.b64encode(form.photo.data.read()), name=form.photo.data.filename)
            app.db_sess.add(img)
            app.db_sess.commit()
            return redirect("/")
        return render_template("registration_master.html", title='Регистрация мастера', form=form)
    else:
        abort(404)


@app.route("/editing_master/<int:master_id>", methods=["GET", "POST"])
@login_required
def editing_master(master_id):
    master = app.db_sess.query(Masters).get(master_id)
    if current_user.id == master.id:
        form = RegisterFormMaster()
        if form.validate_on_submit():
            master.category[0] = app.db_sess.query(Category).filter(Category.name==form.category.data).first()
            master.address = form.address.data
            master.social = form.telegram.data
            master.description = form.description.data
            avatar = list(filter(lambda x: x.type == 'avatar', master.images))
            if avatar:
                avatar[0].data = base64.b64encode(form.photo.data.read())
                avatar[0].name = form.photo.data.filename
            else:
                img = Images(type='avatar', master_id=master.id, data=base64.b64encode(form.photo.data.read()), name=form.photo.data.filename)
                app.db_sess.add(img)
            app.db_sess.commit()
            return redirect(f"/page_master/{master_id}")
        form.category.data = master.category[0].name
        form.address.data = master.address
        form.telegram.data = master.social
        form.description.data = master.description
        return render_template("registration_master.html", title='Редактирование профиля мастера', form=form, master=master)
    else:
        abort(404)


@app.route("/page_master/<int:user_id>")
def page_master(user_id):
    user = app.db_sess.query(Users).get(user_id)
    img = list(filter(lambda x: x.type == 'avatar', user.images))
    if not img:
        img = app.db_sess.query(Images).filter(Images.type == 'default').first()
    else:
        img = img[0]
    im = Image.open(BytesIO(base64.b64decode(img.data)))
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
    return render_template("page_master.html", master=user, avatar=img, photo=rgb)


async def get_avatar(user):
    avatar = list(filter(lambda x: x.type == 'avatar', user.images))
    if not avatar:
        avatar = app.db_sess.query(Images).filter(Images.type == 'default').first()
    else:
        avatar = avatar[0]
    return user.id, avatar.id


async def main_get_avatar(users):
    tasks = []
    for user in users:
        tasks.append(asyncio.create_task(get_avatar(user)))
    a = await asyncio.gather(*tasks)
    return {m: i for m, i in a}


@app.route('/image/<int:image_id>')
def get_image(image_id):
    image = app.db_sess.query(Images).get(image_id)
    return send_file(BytesIO(base64.b64decode(image.data)), mimetype='image/jpeg')


@app.route("/zapis/<int:id_master>")
def zapis(id_master):
    return render_template("entry.html", master_id=id_master)


@app.route("/adding_service/<int:id>", methods=["GET", "POST"])
def adding_service(id):
    form = DobyslForm()
    if form.validate_on_submit():
        service = Services(master_id=id,
                           name=form.name.data,
                           duration=form.time.data,
                           price=form.price.data)
        app.db_sess.add(service)
        app.db_sess.commit()
        return redirect(f"/page_master/{id}")
    return render_template("dobysl.html", form=form)


@app.route("/delete_service/<int:id>/<int:master_id>", methods=["GET", "POST"])
def delete_service(id, master_id):
    service = app.db_sess.query(Services).filter(Services.id == id).first()
    app.db_sess.delete(service)
    app.db_sess.commit()
    return redirect(f"/page_master/{master_id}")


app.run()
