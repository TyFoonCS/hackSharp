import flask
import sqlite3
import json

app = flask.Flask(__name__)
app.secret_key = "P@ssw0rd"


def session_render_index():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute('select fio, school, points from users order by points')
    table = json.dumps(cursor.fetchall()[::-1])
    print(table)
    lk = 'Личный кабинет'
    lka = '/lk'
    reg = ''
    rega = ''
    enter = 'Выйти'
    entera = "/exit"
    return flask.render_template("index.html", login=flask.session["user"], enter=enter, entera=entera,
                                 rega=rega, reg=reg, lk=lk, lka=lka, table=table)


def anonim_render_index():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute('select fio, school, points from users order by points')
    table = json.dumps(cursor.fetchall()[::-1])
    print(table)
    lk = ""
    lka = ""
    enter = 'Войти'
    entera = "login"
    reg = 'Регистрация'
    rega = "reg"
    return flask.render_template("index.html", login="anonim", enter=enter, entera=entera, rega=rega, reg=reg, lk=lk,
                                 lka=lka, table=table)


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
        type_teacher = flask.request.form.get("teacher")
        print(type_student, type_teacher)
        cursor.execute('select * from users where nick="' + nick + '"')
        ident = cursor.fetchall()
        if len(fio) > 45 or len(nick) > 20 or len(password) > 20:
            return flask.render_template("reg.html", message="Указанные данные слишком длинные!")
        if "" in [fio, nick, password] or (not type_student and not type_teacher) or not school:
            return flask.render_template("reg.html", message="Не все поля заполнены!")
        if ident:
            return flask.render_template("reg.html", message="Такой логин уже занят!")
        if type_student == "on":
            type_user = 0
        else:
            type_user = 1
        print(fio, nick, password, school, type_user)
        sql = 'insert into users values("' + fio + '", "' + nick + '", "' + password + '", "' + school + '", ' + str(
            type_user) + ', "Не указаны", 0)'
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


@app.route('/lk', methods=["POST", "GET"])
def lk():
    if "user" in flask.session:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute('select * from users where nick="'+flask.session["user"]+'"')
        user = cursor.fetchall()[0]
        cursor.execute('select fio, nick, points from users where school="'+user[3]+'"')
        all = json.dumps(cursor.fetchall())
        if flask.request.method == "POST" and flask.request.form.get("target") == "change":
            print(122)
            fio = flask.request.form.get("person_name")
            school = flask.request.form.get("school")
            if fio and school:
                print(144)
                cursor.execute('update users set fio="'+fio+'" where nick="'+flask.session["user"]+'"')
                cursor.execute('update users set school="' + school + '" where nick="' + flask.session["user"] + '"')
                conn.commit()
                return flask.render_template("lk.html", fio=fio, nick=user[1], school=school, achieve=user[5], rate=user[6], type_user=user[4], all=all)
        if flask.request.method == "POST" and flask.request.form.get("target") == "achieve":
            print(12)
            nick = flask.request.form.get("person_achieve_name")
            achieve = flask.request.form.get("person_achieve")
            print(achieve)
            rate = flask.request.form.get("person_achieve_rate")
            cursor.execute('select * from users where nick="'+nick+'"')
            student = cursor.fetchall()[0]
            if student[3] == user[3]:
                if student[5] == "Не указаны":
                    new_achieve = achieve + ";;;;"
                else:
                    new_achieve = student[5] + achieve + ";;;;"
                points = str(student[6] + int(rate))
                print(new_achieve, points)
                cursor.execute('update users set achive="'+new_achieve+'" where nick="'+nick+'"')
                cursor.execute('update users set points="' + points + '" where nick="' + nick + '"')
                conn.commit()

        return flask.render_template("lk.html", fio=user[0], nick=user[1], school=user[3], achieve=user[5], rate=user[6], type_user=user[4], all=all)
    return anonim_render_index()


if __name__ == '__main__':
    app.secret_key = "P@ssw0rd"
    app.run()
