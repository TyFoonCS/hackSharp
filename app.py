import flask
import sqlite3
import json

app = flask.Flask(__name__)


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
        if type_student == "on":
            type_user = 0
        else:
            type_user = 1
        sql = 'insert into users values("' + fio + '", "' + nick + '", "' + password + '", "' + school + '", ' + str(
            type_user) + ', "' + school + '", 0)'
        print(sql)
        cursor.execute(sql)
        conn.commit()
    return flask.render_template("reg.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        login = flask.request.form.get("login")
        password = flask.request.form.get("password")
        cursor.execute('select * from users where nick="'+login+'" and password="'+password+'"')
        res = cursor.fetchall()
        if res:
            flask.render_template("login.html")
    return flask.render_template("login.html")


if __name__ == '__main__':
    app.run()
