from flask import Flask, render_template, redirect, url_for, request, session
from form.loginform import LoginForm
from form.registr import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()

@app.route("/", methods=['GET', 'POST'])
def index1():
    return render_template("index.html", name='')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #db_sess = db_session.create_session()
        #user = db_sess.query(User).filter(User.email == form.email.data).first()
        #if user and user.check_password(form.password.data):
         #   login_user(user, remember=form.remember_me.data)
         #   session['guest'] = user.name
        return redirect("/")
    return render_template('login.html', title='Авторизация', form=form)

@app.route("/masters", methods=['GET', 'POST'])
def masters():
    return render_template("masters.html", name='')

@app.route("/registrate", methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            button_name = request.form['button']
            if button_name == 'mast':
                return render_template("/regmas")
            if button_name == 'klint':
                return redirect('/login')
    #   if form.password.data != form.password_again.data:
     #       return render_template('register.html', title='Регистрация',
      #                             form=form,
       #                            message="Пароли не совпадают")
        #db_sess = db_session.create_session()
        #if db_sess.query(User).filter(User.email == form.email.data).first():
         #   return render_template('register.html', title='Регистрация',
          #                         form=form,
           #                        message="Такой пользователь уже есть")
    return render_template("registrate.html", name='', form=form)

@app.route("/mast", methods=["POST"])
def move_forward():
    return "fghjk"

if __name__ == '__main__':
    main()