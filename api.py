from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_USER'] = 'artemis_user'
app.config['MYSQL_PASSWORD'] = 'TeamArtemis2021!'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/logs", methods=['GET', 'POST'])
def logs():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('''SELECT user, host FROM mysql.user''')
        rv = cur.fetchall()
        return str(rv)
