from flask import Flask, render_template

app = Flask(__name__)


@app.route('/reg', methods=["POST", "GET"])
def index():
    return render_template("reg.html")


if __name__ == '__main__':
    app.run()
