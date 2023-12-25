import mangum
from mangum import Mangum

from keras_prediction_via_web_app import flask_web_app

lambda_handler=Mangum(flask_web_app)

if __name__ == '__main__':
    flask_web_app.run(host='0.0.0.0', port=8000, debug=True)

