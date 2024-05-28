import requests

from data.db_session import global_init, create_session
from flask import Flask, render_template, redirect, send_file
import string
from random import choice
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from flask_restful import abort, Api
from api.users_resources import UsersResources, UsersListResources
from api.services_resources import ServicesResources, ServicesListResources
from api.images_resources import ImagesResources, ImagesListResources
from api.appointments_resources import AppointmentsResources, AppointmentsListResources
from data.category import Category
from data.images import Images
from data.users import Users, Masters, Clients
from data.services import Services
from data.appointments import Appointments
from form.login_form import LoginForm
from form.registration_form import RegistrationForm
from form.registration_master_form import RegistrationMasterForm
from form.adding_service_form import AddingServiceForm
from form.sign_up_form import SignUpForm
from form.adding_works_form import AddingWorksForm
from datetime import datetime
from PIL import Image
import base64
from io import BytesIO
import asyncio


class App(Flask):
    def __init__(self, import_name: str):
        super().__init__(import_name)
        self.config['SECRET_KEY'] = 'zxc_secret_key'
        global_init()
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
        db_sess = create_session()
        categories = db_sess.query(Category).all()
        if len(categories) == 0:
            categories = [Category(name='Мастер маникюра(педикюра)'), Category(name='Парикмахер'), Category(name='Визажист')]
            for c in categories:
                db_sess.add(c)
            db_sess.commit()
        db_sess.close()

    def check_photo(self):
        db_sess = create_session()
        photos = db_sess.query(Images).all()
        if len(list(filter(lambda x: x.type == 'default', photos))) == 0:
            with open('static/img/default.jpg', 'rb') as f:
                d = base64.b64encode(f.read())
            img = Images(name='default.jpg', data=d, type='default')
            db_sess.add(img)
            db_sess.commit()
        db_sess.close()


app = App(__name__)


@app.login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    users = db_sess.query(Users).filter_by(id=user_id).first()
    db_sess.close()
    return users


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route("/", methods=['GET', 'POST'])
def index():
    sess = create_session()
    login_user(sess.query(Users).filter(Users.type == 'Clients').first())
    sess.close()
    if not current_user.is_authenticated or current_user.type == 'Clients':
        return render_template("index.html", title='Главная страница')
    else:
        return redirect(f'/page_master/{current_user.id}')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                db_sess.close()
                return redirect("/")
            db_sess.close()
            return render_template('login.html', title='Авторизация', message='Неверный пароль', form=form)
        db_sess.close()
        return render_template('login.html', title='Авторизация', message='Такого пользователя нет', form=form)
    db_sess.close()
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/masters/<type>")
def masters(type):
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = create_session()
    users = db_sess.query(Masters).all()
    users = list(filter(lambda x: x.category[0].name == type, users))
    ids_avatars = asyncio.run(main_get_avatar(users))
    res = render_template("masters.html", users=users, avatars=ids_avatars, title=type)
    db_sess.close()
    return res


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("registration.html", name='', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            db_sess.close()
            return render_template("registration.html", name='', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        if form.user.data == 'Мастер':
            user = Masters()
        else:
            user = Clients()
        user.nick_name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        db_sess.close()
        if form.user.data == 'Мастер':
            return redirect(f"/registration_master/{user.id}")
        return redirect('/')
    db_sess.close()
    return render_template("registration.html", form=form)


@app.route("/registration_master/<int:master_id>", methods=["GET", "POST"])
def registration_master(master_id):
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    master = db_sess.query(Masters).get(master_id)
    if current_user.id == master.id and master.registrate is False:
        form = RegistrationMasterForm()
        if form.validate_on_submit():
            master.category.append(db_sess.query(Category).filter(Category.name==form.category.data).first())
            master.address = form.address.data
            master.social = form.telegram.data
            master.description = form.description.data
            master.registrate = True
            img = Images(type='avatar', master_id=master.id, data=base64.b64encode(form.photo.data.read()), name=form.photo.data.filename)
            db_sess.add(img)
            db_sess.commit()
            db_sess.close()
            return redirect("/")
        return render_template("registration_master.html", title='Регистрация мастера', form=form)
    else:
        abort(404)
    db_sess.close()


@app.route("/editing_master/<int:master_id>", methods=["GET", "POST"])
def editing_master(master_id):
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    master = db_sess.query(Masters).get(master_id)
    if current_user.id == master.id:
        form = RegistrationMasterForm()
        if form.validate_on_submit():
            master.category[0] = db_sess.query(Category).filter(Category.name==form.category.data).first()
            master.address = form.address.data
            master.social = form.telegram.data
            master.description = form.description.data
            avatar = list(filter(lambda x: x.type == 'avatar', master.images))
            if avatar:
                avatar[0].data = base64.b64encode(form.photo.data.read())
                avatar[0].name = form.photo.data.filename
            else:
                img = Images(type='avatar', master_id=master.id, data=base64.b64encode(form.photo.data.read()), name=form.photo.data.filename)
                db_sess.add(img)
            db_sess.commit()
            db_sess.close()
            return redirect(f"/page_master/{master_id}")
        form.category.data = master.category[0].name
        form.address.data = master.address
        form.telegram.data = master.social
        form.description.data = master.description
        res = render_template("registration_master.html", title='Редактирование профиля мастера', form=form, master=master)
        db_sess.close()
        return res
    else:
        abort(404)
    db_sess.close()


@app.route("/page_master/<int:master_id>")
def page_master(master_id):
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    user = db_sess.query(Users).filter(Users.id == master_id).first()
    works = list(filter(lambda x: x.type == 'works', user.images))
    avatar = list(filter(lambda x: x.type == 'avatar', user.images))
    if not avatar:
        avatar = db_sess.query(Images).filter(Images.type == 'default').first()
    else:
        avatar = avatar[0]
    im = Image.open(BytesIO(base64.b64decode(avatar.data)))
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
    res = render_template("page_master.html", master=user, avatar=avatar, photo=rgb,
                          title=user.nick_name, works=works)
    db_sess.close()
    return res


@app.route("/editing_works/<int:master_id>")
def editing_works(master_id):
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    master = db_sess.query(Users).filter(Users.id == master_id).first()
    images = list(filter(lambda x: x.type == 'works', master.images))
    res = render_template('editing_works.html', title='Изменение примеров', images=images)
    db_sess.close()
    return res


@app.route("/adding_works/<int:master_id>", methods=["GET", "POST"])
def adding_works(master_id):
    if not current_user.is_authenticated:
        return redirect('/')
    form = AddingWorksForm()
    if form.validate_on_submit():
        db_sess = create_session()
        image = Images(
            type='works',
            master_id=master_id,
            data=base64.b64encode(form.photo.data.read()),
            name=form.photo.data.filename,
            description=form.description.data
        )
        db_sess.add(image)
        db_sess.commit()
        db_sess.close()
        return redirect(f'/editing_works/{master_id}')
    return render_template('adding_works.html', form=form)


@app.route("/delete_work/<int:id>")
@login_required
def delete_work(id):
    db_sess = create_session()
    img = db_sess.query(Images).filter(Images.id==id).first()
    master_id = img.master_id
    db_sess.delete(img)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/editing_works/{master_id}')


async def get_avatar(user):
    db_sess = create_session()
    avatar = list(filter(lambda x: x.type == 'avatar', user.images))
    if not avatar:
        avatar = db_sess.query(Images).filter(Images.type == 'default').first()
    else:
        avatar = avatar[0]
    res = (user.id, avatar.id)
    db_sess.close()
    return res


async def main_get_avatar(users):
    tasks = list(map(lambda x: asyncio.create_task(get_avatar(x)), users))
    ids = await asyncio.gather(*tasks)
    return {m: i for m, i in ids}


@app.route('/image/<int:image_id>')
def get_image(image_id):
    db_sess = create_session()
    image = db_sess.query(Images).filter(Images.id==image_id).first()
    res = send_file(BytesIO(base64.b64decode(image.data)), mimetype='image/jpeg')
    db_sess.close()
    return res


@app.route("/appointments/")
def main_appointments():
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    appointments = db_sess.query(Appointments).filter(
        (Appointments.master_id == current_user.id) | (Appointments.client_id == current_user.id)).all()
    if len(appointments) > 5:
        res = redirect('/appointments/1')
    else:
        masters_names = {x.master_id: db_sess.query(Users).filter(Users.id == x.master_id).first().nick_name
                         for x in appointments}
        res = render_template('appointments.html', appointments=appointments, page=0, title='Записи',
                              masters=masters_names)
    db_sess.close()
    return res


@app.route("/appointments/<int:page>")
def page_appointments(page):
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    appointments = db_sess.query(Appointments).filter(
        (Appointments.master_id == current_user.id) | (Appointments.client_id == current_user.id)).all()
    pages = len(appointments) // 5 if len(appointments) % 5 == 0 else len(appointments) // 5 + 1
    appointments = appointments[5 * (page - 1):5 * page] if pages == page else appointments[5 * (page - 1):-1]
    masters_names = {x.master_id: db_sess.query(Users).filter(Users.id == x.master_id).first().nick_name
                     for x in appointments}
    res = render_template('appointments.html', appointments=appointments, page=page, pages=pages,
                          title='Записи', masters=masters_names)
    db_sess.close()
    return res


@app.route("/adding_service/<int:id>", methods=["GET", "POST"])
def adding_service(id):
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    form = AddingServiceForm()
    if form.validate_on_submit():
        service = Services(master_id=id,
                           name=form.name.data,
                           duration=form.time.data,
                           price=form.price.data)
        db_sess.add(service)
        db_sess.commit()
        db_sess.close()
        return redirect(f"/page_master/{id}")
    return render_template("adding_service.html", form=form)


@app.route("/delete_service/<int:id>/<int:master_id>")
@login_required
def delete_service(id, master_id):
    db_sess = create_session()
    service = db_sess.query(Services).filter(Services.id == id).first()
    db_sess.delete(service)
    db_sess.commit()
    db_sess.close()
    return redirect(f"/page_master/{master_id}")


@app.route("/sign_up/<int:id>", methods=["GET", "POST"])
def sign_up(id):
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = create_session()
    master = db_sess.query(Users).filter(Users.id == id).first()
    choices = {f'{x.name} {x.duration} {x.price}': x for x in master.services}
    form = SignUpForm()
    form.choice.choices = list(choices.keys())
    if form.validate_on_submit():
        dt = datetime.combine(form.date.data, form.time.data)
        appointment = Appointments(master_id=id,
                           client_id=current_user.id,
                           datetime=dt)
        appointment.services.extend(list(map(lambda x: choices[x], form.choice.data)))
        db_sess.add(appointment)
        db_sess.commit()
        db_sess.close()
        return redirect(f"/page_master/{id}")
    return render_template("sign_up.html", form=form, master=master)


@app.route("/delete_appointment/<int:id>")
@login_required
def delete_appointment(id):
    db_sess = create_session()
    appointments = db_sess.query(Appointments).filter(Appointments.id == id).first()
    db_sess.delete(appointments)
    db_sess.commit()
    db_sess.close()
    return redirect(f"/appointments")


app.run()
