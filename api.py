import datetime
import os

import boto3
from botocore.exceptions import ClientError
from flask import Flask, request, session, redirect, url_for, jsonify, send_from_directory, Response, abort, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename


app = Flask(__name__)
mysql = MySQL(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}

app.config['MYSQL_USER'] = 'artemis_user'
app.config['MYSQL_PASSWORD'] = 'TeamArtemis2021!'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = "ASecretKey"
app.config['UPLOAD_FOLDER'] = '.'

BUCKET = 'nasaappsartemis'


def parse_logs_form(req, target):
    app.logger.debug(f'Looking for {target}')
    if target == 'logdate':
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if target == 'username':
        return session['username']
    try:
        value = req.form[target]
        if value:
            return value
        return None
    except:
        return None


def parse_logs_json(req, target):
    app.logger.debug(f'Looking for {target}')
    if target == 'logdate':
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if target == 'username':
        return session['username']
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
        if session['role'] == 'public':
            abort(401)
        values = ['username', 'logdate', 'logtext', 'logtype', 'mediaID', 'hardware', 'UpdateID', 'hashtag', 'approvelog']
        app.logger.debug(f'get_json: {request.get_json()}')

        if request.get_json():
            converted = tuple([parse_logs_json(request.get_json(), val) for val in values])
        else:
            converted = tuple([parse_logs_form(request, val) for val in values])
        app.logger.debug(f'converted: {converted}')
        sql = 'INSERT INTO `logs_db`.`logs` (username, logdate, logtext, logtype, mediaID, hardware, UpdateID, hashtag, approvelog) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

        cur = mysql.connection.cursor()
        cur.execute(sql, converted)
        mysql.connection.commit()

        return "Successfully added new log"


@app.route("/logs/add")
def add_logs():
    if 'username' not in session:
        return redirect(url_for('login'))
    app.logger.debug(session['role'])
    app.logger.debug(session['role'] == 'mission control')
    app.logger.debug(session['role'] == 'mission control' or session['role'] == 'researcher')
    if session['role'] == 'public':
        abort(401)

    return send_from_directory('static', 'logs.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        if 'file' not in request.files:
            flash('No file part')
            return redirect('medias/add')

        file = request.files['file']
        app.logger.debug(type(file))
        if file.filename == '':
            flash('No selected file')
            return redirect('medias/add')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        imageref, videoref, audioref = None, None, None
        if filename.rsplit('.', 1)[1].lower() in ['pdf', 'png', 'jpg', 'jpeg', 'gif']:
            #https://nasaappsartemis.s3.us-east-2.amazonaws.com/DreamChaser.jpg
            imageref = f'https://{BUCKET}.s3.us-east-2.amazonaws.com/{filename}'
        if filename.rsplit('.', 1)[1].lower() in ["mp4"]:
            videoref = f'https://{BUCKET}.s3.us-east-2.amazonaws.com/{filename}'
        if filename.rsplit('.', 1)[1].lower() in ['mp3']:
            audioref = f'https://{BUCKET}.s3.us-east-2.amazonaws.com/{filename}'

        app.logger.debug(os.environ.get('AWS_SECRET_ACCESS_KEY'))
        # Upload the file
        app.logger.debug(f'filename: {filename}')
        app.logger.debug(f'imageref: {imageref}  videoref: {videoref}  audioref: {audioref}')
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(filename, BUCKET, os.path.basename(filename), ExtraArgs={'ACL':'public-read'})
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except ClientError as e:
            app.logger.error("Error Uploading.")
            app.logger.error(e)

        app.logger.debug(f'S3 Response: {response}')

        sql = 'INSERT INTO `logs_db`.`media` (imageref, videoref, audioref) VALUES (%s, %s, %s)'

        cur = mysql.connection.cursor()
        cur.execute(sql, (imageref, videoref, audioref))
        mysql.connection.commit()

        return "Successfully added new media"


@app.route("/medias/add")
def add_media():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session['role'] == 'public':
        abort(401)
    return send_from_directory('static', 'media.html')


@app.route("/users", methods=['GET'])
def users():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        if session['role'] != 'mission control':
            cur = mysql.connection.cursor()
            cur.execute(f"SELECT firstname, lastname FROM logs_db.users WHERE logs_db.users.username='{session['username']}';")
            rv = cur.fetchall()
            return jsonify(rv)
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT firstname, lastname FROM logs_db.users;")
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
            session['role'] = user_data['role']
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return send_from_directory('static', 'login.html')


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


@app.errorhandler(401)
def custom_401(error):
    return Response('<Why access is denied string goes here...>', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})
