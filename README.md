# Pneumonia-Evaluation-webapp

Webapp interface to Evaluate chest x-ray image for pneumonia using Trained CNN model.

# Demonstration-:
https://user-images.githubusercontent.com/99067991/203352471-35cfa2f1-7f26-4922-8a65-7566bd81bc83.mp4

# How to setup -:

1) clone repository.
2) keep the structure of directories same do not change names of 'staticFiles' and 'templates' folder unless you know what you are doing.
3) Download [p1.h5](https://drive.google.com/file/d/1U7O_mecksPVFuM7ZbEkz1wpwwDI97ccr/view?usp=sharing) model file and add it to any directory on your pc.
4) Give path to the p1.h5 file in following codeline (main.py)

    `model = tf.keras.models.load_model('path here')`
  
5) Download and install [MySQL](https://dev.mysql.com/downloads/installer/), you can Refer to [this](https://www.javatpoint.com/how-to-install-mysql) guide if you dont know what options to choose during installation.
6) Open MySQL Workbench login to localhost and run following command in Query tab.

        CREATE DATABASE IF NOT EXISTS `pythonlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
        USE `pythonlogin`;

        CREATE TABLE IF NOT EXISTS `accounts` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `username` varchar(50) NOT NULL,
            `password` varchar(255) NOT NULL,
            `email` varchar(100) NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

        INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com');
        
7) Put your MySQl database password in app.config(main.py).

        # Enter your database connection details below
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'Your password here'
        app.config['MYSQL_DB'] = 'pythonlogin'
 
8) Run main.py



# References

https://stackoverflow.com/questions/23327293/flask-raises-templatenotfound-error-even-though-template-file-exists

https://thinkinfi.com/upload-and-display-image-in-flask-python/

https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/

https://codeshack.io/login-system-python-flask-mysql/
