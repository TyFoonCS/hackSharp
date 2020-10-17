import flask
import sqlite3
import json

app = flask.Flask(__name__)
app.secret_key = "P@ssw0rd"


def session_render_index():
    lk = 'Личный кабинет'
    lka = '/lk'
    reg = ''
    rega = ''
    enter = 'Выйти'
    entera = "/exit"
    return flask.render_template("index.html", login=flask.session["user"], enter=enter, entera=entera,
                                 rega=rega, reg=reg, lk=lk, lka=lka)


def anonim_render_index():
    lk = ""
    lka = ""
    enter = 'Войти'
    entera = "login"
    reg = 'Регистрация'
    rega = "reg"
    return flask.render_template("index.html", login="anonim", enter=enter, entera=entera, rega=rega, reg=reg, lk=lk,
                                 lka=lka)


@app.route('/reg', methods=["POST", "GET"])
def reg():
    if flask.request.method == "POST":
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        fio = flask.request.form.get("person_name")
        nick = flask.request.form.get("person_login")
        password = flask.request.form.get("person_pass")
        school = flask.request.form.get("school")
        type_student = flask.request.form.get("student")
        cursor.execute('select * from users where nick="' + nick + '"')
        ident = cursor.fetchall()
        if ident:
            return flask.render_template("reg.html", nick_reg="Такой логин уже занят!")
        if type_student == "on":
            type_user = 0
        else:
            type_user = 1
        sql = 'insert into users values("' + fio + '", "' + nick + '", "' + password + '", "' + school + '", ' + str(
            type_user) + ', "' + school + '", 0)'
        print(sql)
        cursor.execute(sql)
        conn.commit()
        flask.session["user"] = nick
        return session_render_index()
    return flask.render_template("reg.html", nick_reg="Логин")


@app.route('/login', methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        login = flask.request.form.get("login")
        password = flask.request.form.get("password")
        cursor.execute('select * from users where nick="' + login + '" and password="' + password + '"')
        res = cursor.fetchall()
        if res:
            if not "user" in flask.session:
                flask.session["user"] = login
            return session_render_index()
        else:
            return flask.render_template("login.html", message="Данные не верны!")
    return flask.render_template("login.html", message="")


@app.route('/')
def index():
    if "user" in flask.session:
        return session_render_index()
    return anonim_render_index()


@app.route('/exit')
def exit():
    if "user" in flask.session:
        flask.session.pop('user', None)
    return anonim_render_index()


@app.route('/lk')
def lk():
    if "user" in flask.session:
        return flask.render_template("lk.html")
    return anonim_render_index()


if __name__ == '__main__':
    app.secret_key = "P@ssw0rd"
    app.run()
