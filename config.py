
import os


# Tell the name & location of the file containing our actual Database to SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_web_app.db')

#IMAGE_FOLDER = ".//keras_prediction_via_web_app//static"
IMAGE_FOLDER = "./images"


#UPLOAD_FOLDER = 'path/to/upload/folder'



#MY_API_ID =


# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(24)])
#SECRET_KEY = "#d#JCqTTW\nilK\\7m\x0bp#\tj~#H"


#SECRET_KEY = ""