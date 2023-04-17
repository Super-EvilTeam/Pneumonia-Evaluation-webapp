from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify,Response
from threading import Thread
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import re
import os
import math
from zipfile import ZipFile

class Login:
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
            
class Register:
    def __init__(self,username,password,confirm_password,email):
        self.username = username
        self.password = password
        self.confirm_password = confirm_password
        self.email = email
        
    def check_ExistingUser(self):
        self.cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        self.cursor.execute('SELECT * FROM accounts WHERE username = %s', (self.username,))
        self.account = self.cursor.fetchone()
        if self.account != None:
            return True
        return False
    
    def validate_Info(self):
        msg = ''
        if not re.match(r'[^@]+@[^@]+\.[^@]+', self.email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', self.username):
            msg = 'Username must contain only characters and numbers!'
        elif not self.username or not self.password or not self.email:
            msg = 'Please fill out the form!'
        elif self.password != self.confirm_password:
            msg = 'Passwords do not match'
        else:
            msg = 'Valid'
        return msg
    
    def check_Emptyform(self):
        if request.method == 'POST':
            return True
        return False
    
    def add_User(self):
        self.cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (self.username, self.password, self.email,))
        mysql.connection.commit()

class Logout:
    def __init__(self):
        pass
    
    def end_Session(self):
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)

class Home:
    def __intit__(self):
        pass
    
    def active_Session(self):
        if 'loggedin' in session:
            return True
        return False

class Profile(Login):
    def __init__(self):
        pass
    
    def user_Info(self):
        self.cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        self.cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = self.cursor.fetchone()
        return account
    
class Result():
    def __init__(self):
        pass
    
    def prepare(self,filepath):
        IMG_SIZE = 224
        img_array =cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        new_array=cv2.resize(img_array, (IMG_SIZE,IMG_SIZE))
        return new_array.reshape(-1, IMG_SIZE,IMG_SIZE,1)

    def show_Result(self):
        uploaded_img = request.files['uploaded-file']# Upload file flask
        img_filename = secure_filename(uploaded_img.filename)# Extracting uploaded data file name
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))# Upload file to database (defined uploaded folder in static path)
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)# Storing uploaded file path in flask session
        img_file_path = session.get('uploaded_img_file_path', None)# Retrieving uploaded file path from session
        prediction = model.predict([self.prepare(img_file_path)])
        CATEGORIES = ['Affected','Normal']
        msg = CATEGORIES[int(prediction[0][0])]
        return img_file_path,msg

class patterns():
    def __init__(self):
        pass
    

    def show_pattern(self,layer_num):
        start = (layer_num-1)*18  # Calculate the starting index of images to display
        end = start + 18  # Calculate the ending index of images to display
        folder_path = 'D:\Sumit\BE_Final_Year_Project\Pneumonia-Evaluation-webapp-main\plots'
        files = os.listdir(folder_path)  # Get the list of files in the folder
        
        # Calculate the number of rows and columns in the subplot grid
        num_cols = 6
        num_rows = math.ceil((end - start) / num_cols)
        
        # Create the subplot grid
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(10,10))
        
        # Iterate over the files and plot the images in the subplot grid
        for i in range(start, end):
            if i >= len(files):  # Break the loop if all images have been displayed
                break
            img_path = os.path.join(folder_path, files[i])
            img = plt.imread(img_path)
            row = (i - start) // num_cols
            col = (i - start) % num_cols
            axes[row, col].imshow(img)
            axes[row, col].axis('off')
        
        plt.subplots_adjust(wspace=0, hspace=0)  # Remove the spacing between the subplots
        print('done')
        # plt.show()




app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.secret_key = '2c20aa641c0c82029850dec9c8213d46807f6e8e6d9a9ee90e7516a2345ee055'
app.config['UPLOAD_FOLDER'] = os.path.join('staticFiles', 'uploads')
app.config['PATTERNS'] = os.path.join('staticFiles', 'plots')
#database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'


mysql = MySQL(app)# Intialize MySQL
model = tf.keras.models.load_model('staticFiles\Trained models\p1.h5')# Load model

#http://localhost:5000/ - this will be login page, which will use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        login_user = Login(request.form['username'],request.form['password'])
        if login_user.account_Exist():
            login_user.create_session()
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

# http://localhost:5000/pythonlogin/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
     logout_user = Logout()
     logout_user.end_Session()
     return redirect(url_for('login'))

# http://localhost:5000/pythonlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'confirm_password' in request.form and 'email' in request.form:
        Register_user = Register(request.form['username'],request.form['password'],request.form['confirm_password'],request.form['email'])
        validity= Register_user.validate_Info()
        if Register_user.check_ExistingUser():
            msg = 'Account already exists!'
        elif validity != 'Valid':
            msg = validity
        elif validity == 'Valid':
            Register_user.add_User()
            msg = 'You have successfully registered!'
        elif Register_user.check_Emptyform():
            msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythonlogin/home - this will be the home page, only accessible for loggedin users        
@app.route('/pythonlogin/home', methods=['GET', 'POST'])
def home():
    home_page = Home()
    if home_page.active_Session():
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# http://localhost:5000/pythonlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    user_profile = Profile()
    if 'loggedin' in session: # Check if user is loggedin
        account = user_profile.user_Info() # We need all the account info for the user so we can display it on the profile page
        return render_template('profile.html', account=account)# Show the profile page with account info
    return redirect(url_for('login')) # User is not loggedin redirect to login page

@app.route("/Result", methods=['GET', 'POST'])
def result():
    user_result = Result()
    if request.method == 'POST':
        uploaded_image,prediction = user_result.show_Result()
        return render_template('Result.html', uploaded_image = uploaded_image,prediction = prediction)

@app.route('/run-prediction', methods=['POST'])
def run_prediction():
    image_path = request.form['image_path'] # get the image path from the request data
  # perform the prediction using the image path
    if not os.path.exists('plots'):
        os.makedirs('plots')

    # Load an image
    image = cv2.imread(image_path , cv2.IMREAD_GRAYSCALE)

    # Resize the image to (224, 224) and add a channel dimension
    input_image = cv2.resize(image, (224, 224)).reshape(-1, 224, 224, 1)

    # Get the output activations for all layers in the model
    layer_outputs = [layer.output for layer in model.layers]

    # Create a new model that takes the input image and outputs the activations for all layers
    activation_model = tf.keras.models.Model(inputs=model.input, outputs=layer_outputs)

    # Get the activations for all layers for the input image
    activations = activation_model.predict(input_image)

    # Specify the filters to visualize in each layer
    layer_filters = {
        0: [1, 5, 7, 10, 11, 13, 15, 16, 17, 20, 21, 22, 23, 24, 25, 36, 43, 62],
        1: [1, 5, 7, 10, 11, 13, 15, 16, 17, 20, 21, 22, 23, 24, 25, 36, 43, 62],
        2: [1, 5, 7, 10, 11, 13, 15, 16, 17, 20, 21, 22, 23, 24, 25, 36, 43, 62],
        3: [1, 5, 7, 10, 11, 13, 15, 16, 17, 20, 21, 22, 23, 24, 25, 36, 43, 62],
        4: [1, 5, 7, 10, 11, 13, 15, 16, 17, 20, 21, 22, 23, 24, 25, 36, 43, 62],
        5: [1, 5, 7, 10, 11, 13, 15, 16, 17, 20, 21, 22, 23, 24, 25, 36, 43, 62]
    }

    # Loop over the layers and filters to visualize and plot the activations as heatmaps
    for layer_index, filters in layer_filters.items():
        layer_activations = activations[layer_index]
        for filter_index in filters:
            activations_for_filter = layer_activations[:, :, :, filter_index]
            plt.matshow(activations_for_filter[0, :, :], cmap='viridis')
            plt.savefig(f'plots/layer{layer_index}_filter{filter_index}.png')
            plt.close()
    # return the HTML as a response
    return 'success'
    
@app.route('/get_patterns', methods=['POST'])
def get_patterns():
    selected_option = request.form['selected_option']
    layer_num = int(selected_option.split('_')[1])
    print(layer_num)

    obj = patterns()
    def run_show_pattern():
        obj.show_pattern(layer_num)

    # Create a new thread and start it
    thread = Thread(target=run_show_pattern)
    thread.start()

    return 'success'

    # Use the layer number to get the appropriate patterns
    # if layer_num == 1:
    #     patterns = get_patterns_from_layer_0()
    # elif layer_num == 2:
    #     patterns = get_patterns_from_layer_1()
    # elif layer_num == 3:
    #     patterns = get_patterns_from_layer_2()
    # elif layer_num == 4:
    #     patterns = get_patterns_from_layer_3()
    # elif layer_num == 5:
    #     patterns = get_patterns_from_layer_4()
    # else:
    #     patterns = []
    # return jsonify(patterns)

if __name__ == "__main__":
    app.run(debug=True)