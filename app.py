import flask

app = flask.Flask(__name__)


@app.route('/reg', methods=["POST", "GET"])
def reg():
    if flask.request.method == "POST":
        fio = flask.request.form.get("person_name")
        print(fio)
    return flask.render_template("reg.html")


if __name__ == '__main__':
    app.run()
