from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()

@app.route("/", methods=['GET', 'POST'])
def index1():
    return render_template("index.html", name='')

if __name__ == '__main__':
    main()