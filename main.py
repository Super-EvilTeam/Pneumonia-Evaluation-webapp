from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import cv2
import tensorflow as tf
import re
import os


class login_user:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        
    def account_Exist(self):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (self.username, self.password,))
        self.account = cursor.fetchone()
        if self.account == None:
            return False
        return True
        
    def create_session(self):
        if self.account:
            session['loggedin'] = True
            session['id'] = self.account['id']
            session['username'] = self.account['username']

#model = tf.keras.models.load_model('E:\project final year\pneumonia\code\main_code\p1.h5')
CATEGORIES = ['Affected','Normal']
def prepare(filepath):
    IMG_SIZE = 224
    img_array =cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array=cv2.resize(img_array, (IMG_SIZE,IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE,IMG_SIZE,1)

    
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '2c20aa641c0c82029850dec9c8213d46807f6e8e6d9a9ee90e7516a2345ee055'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

# # http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     # Output message if something goes wrong...
#     msg = ''
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         password = request.form['password']
#         # Check if account exists using MySQL
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
#         # Fetch one record and return result
#         account = cursor.fetchone()
#         # If account exists in accounts table in out database
#         if account:
#             # Create session data, we can access this data in other routes
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['username'] = account['username']
#             # Redirect to home page
#             return redirect(url_for('home'))
#         else:
#             # Account doesnt exist or username/password incorrect
#             msg = 'Incorrect username/password!'
#     # Show the login form with message (if any)
#     return render_template('login.html', msg=msg)
        
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        login_instance = login_user(username,password)
        if login_instance.account_Exist():
            login_instance.create_session()
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/pythonlogin/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        image = request.files['image']  # get file
        return redirect(url_for('result', image=image))
    return render_template('home.html')


@app.route("/Result", methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        # Retrieving uploaded file path from session
        img_file_path = session.get('uploaded_img_file_path', None)
        # Display image in Flask application web page
        prediction = model.predict([prepare(img_file_path)])
        msg = CATEGORIES[int(prediction[0][0])]
        return render_template('Result.html', user_image = img_file_path,msg = msg)

if __name__ == "__main__":
    app.run(debug=True)