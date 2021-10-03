import datetime

from flask import Flask, request, session, redirect, url_for, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)
mysql = MySQL(app)


app.config['MYSQL_USER'] = 'artemis_user'
app.config['MYSQL_PASSWORD'] = 'TeamArtemis2021!'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = "ASecretKey"


def parse_logs_form(req, target):
    app.logger.debug(f'Looking for {target}')
    if target == 'logdate':
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        return req.form[target]
    except:
        return None


def parse_logs_json(req, target):
    app.logger.debug(f'Looking for {target}')
    if target == 'logdate':
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        return req[target]
    except:
        return None


@app.route("/logs", methods=['GET', 'POST'])
def logs():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM logs_db.logs''')
        rv = cur.fetchall()
        return jsonify(rv)

    if request.method == 'POST':
        values = ['username', 'logdate', 'logtext', 'hardware', 'UpdateID', 'hashtag', 'approvelog']
        app.logger.debug(f'get_json: {request.get_json()}')

        if request.get_json():
            converted = tuple([parse_logs_json(request.get_json(), val) for val in values])
        else:
            converted = tuple([parse_logs_form(request, val) for val in values])
        app.logger.debug(f'converted: {converted}')
        sql = 'INSERT INTO `logs_db`.`logs` (username, logdate, logtext, hardware, UpdateID, hashtag, approvelog) VALUES (%s, %s, %s, %s, %s, %s, %s)'

        cur = mysql.connection.cursor()
        cur.execute(sql, converted)
        mysql.connection.commit()

        return "Successfully added new log"


@app.route("/medias", methods=['GET', 'POST'])
def media():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM logs_db.media''')
        rv = cur.fetchall()
        return jsonify(rv)

    if request.method == 'POST':
        media_values = ['imageref', 'videoref', 'audioref']
        app.logger.debug(f'get_json: {request.get_json()}')

        if request.get_json():
            converted = tuple([parse_logs_json(request.get_json(), val) for val in media_values])
        else:
            converted = tuple([parse_logs_form(request, val) for val in media_values])
        app.logger.debug(f'converted: {converted}')
        sql = 'INSERT INTO `logs_db`.`media` (imageref, videoref, audioref) VALUES (%s, %s, %s)'

        cur = mysql.connection.cursor()
        cur.execute(sql, converted)
        mysql.connection.commit()

        return "Successfully added new media"


@app.route("/users", methods=['GET'])
def users():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('''SELECT firstname, lastname FROM logs_db.users''')
        rv = cur.fetchall()
        return jsonify(rv)


@app.route('/')
def index():
    app.logger.debug(f'session{session}')
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = get_user(request.form['username'])

        if not user_data:
            return redirect(url_for('login'))
        app.logger.debug(f"login form data: {request.form}")
        # Plain text is BAD! But hackathon, so quick and very dirty!!
        if request.form['password'] == user_data['password']:
            session['username'] = request.form['username']
            session['approval'] = user_data['approval']
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return '''
                <form action='login' method='POST'>
                 <input type='text' name='username' id='username' placeholder='username'/>
                 <input type='password' name='password' id='password' placeholder='password'/>
                 <input type='submit' name='submit'/>
                </form>
                '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


def get_user(username):
    cur = mysql.connection.cursor()
    cur.execute(f'select * from logs_db.users where logs_db.users.username = "{username}";')
    user_data = cur.fetchall()
    app.logger.debug(f'retrieved userdata: {user_data}')
    if len(user_data) > 1:
        raise ValueError("More than one user with that username")
    elif len(user_data) < 1:
        return None

    return user_data[0]
