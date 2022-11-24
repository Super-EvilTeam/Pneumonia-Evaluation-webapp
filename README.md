# Pneumonia-Evaluation-webapp

Webapp interface to Evaluate chest x-ray image for pneumonia using Trained CNN model

# Demonstration-:
https://user-images.githubusercontent.com/99067991/203352471-35cfa2f1-7f26-4922-8a65-7566bd81bc83.mp4

# How to setup -:

1) clone repository.
2) keep the structure of directories same do not change names of 'staticFiles' and 'templates' folder unless you know what you are doing.
3) Download [p1.h5](https://drive.google.com/file/d/1U7O_mecksPVFuM7ZbEkz1wpwwDI97ccr/view?usp=sharing) model file and add it to any directory on your pc.
4) Give path to the p1.h5 file in following codeline (main.py)

    `model = tf.keras.models.load_model('path here')`
  
5) Download and install [MySQL](https://dev.mysql.com/downloads/installer/), you can Refer to [this](https://www.javatpoint.com/how-to-install-mysql) guide if you dont know what options to choose during installation.
6) 


# References

https://stackoverflow.com/questions/23327293/flask-raises-templatenotfound-error-even-though-template-file-exists

https://thinkinfi.com/upload-and-display-image-in-flask-python/

https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/

https://codeshack.io/login-system-python-flask-mysql/
