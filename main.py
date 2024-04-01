from flask import Flask, render_template, redirect, url_for, request, session
from form.loginform import LoginForm


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

if __name__ == '__main__':
    main()