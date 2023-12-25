import os
import flask
from flask import render_template
#from flask import send_from_directory
from .models import db, Table_datasetphotos_names
import numpy as np
import json
import pickle
import requests
from PIL import Image
from io import BytesIO
import base64
import mangum
from mangum import Mangum



# WEB API setup
flask_web_app = flask.Flask(__name__, static_folder="./keras_prediction_via_web_app/static")
flask_web_app.config["DEBUG"] = True
flask_web_app.config.from_object('config')

# Here we "ASSOCIATE" our API with the SQLAlchemy Connection Object
db.init_app(flask_web_app)

# POPULATE the Tables of the created EMPTY "flask_web_app.db" Database
# The Flask functionality of INTERACTING with SQLAlchemy requires an ACTIVE "CONTEXT" for our API
app_ctx = flask_web_app.app_context()

with app_ctx:
    app_ctx.push()

    db.drop_all()
    db.create_all()

    photo_names_list = os.listdir(flask_web_app.config['IMAGE_FOLDER'])
    

    # Insert info into the TABLE named "Dataset_photos_names" of the empty of the empty "flask_web_app.db" database
    for selected_photo in photo_names_list:
        # No need to instantiate an Object of this Table Class b\c ONLY 1 "instance at a time" of this Class can be in the DB!!!
        new_table_entry = Table_datasetphotos_names(photo_file_names=selected_photo)
        db.session.add(new_table_entry)

    db.session.commit()


# Create URL of Main Page:  http://127.0.0.1:5000 IF locally
@flask_web_app.route("/", methods=["GET"])
def home_page():
    for_webpage_name_list = [var.photo_file_names for var in Table_datasetphotos_names.query.all()]
    # return "<h1>Trying building a FLASK API</h1><p>This site is a prototype API for Image Semantic Segmentation.</p>"

    return render_template('index.html', names=for_webpage_name_list)


# Convert Image.open() object to proper displaying format
def image_to_base64(image):
    # Convert PIL Image to base64 string
    image_buffer = BytesIO()
    image.save(image_buffer, format="PNG")
    image_data = base64.b64encode(image_buffer.getvalue()).decode("utf-8")
    return image_data


@flask_web_app.route('/images/<image_name>')
def show_image(image_name):

    #********ACTUAL images Section************************
    actual_pictures = image_name

    # Path to the image and its mask
    image_path = f"images/{actual_pictures}"
    mask_path = f"actual_masks/{actual_pictures}"


    image = Image.open(image_path)

    # *********API calling Section****************
    url_of_api_prediction_endpoint = "https://flask-api-via-container-project8.azurewebsites.net/predict"

    # Serialized the image as JSON
    image_as_array = np.array(image)
    image_as_json = json.dumps(pickle.dumps(image_as_array).decode("latin-1"))

    # SENDING POST Request
    headers_for_content_and_response = {'Content-Type': 'application/json', 'accept': 'application/json'}
    response_as_json = requests.post(url_of_api_prediction_endpoint, headers=headers_for_content_and_response,
                                     json=image_as_json)

    # Process JSON response

    # Desired length
    print("Mask Shape from Keras model Output", response_as_json.json()['message'])
    Desired_height = response_as_json.json()['message'][0]
    Desired_width = response_as_json.json()['message'][1]
    Desired_length = Desired_height * Desired_width

    # Extract from the POST response the SERIALIZED-AS-JSON IMAGE representing the predicted Mask
    response_as_dict = response_as_json.json()
    response_content_as_byte = response_as_dict['response']
    response_content_raw = json.loads(response_content_as_byte)

    # Make the extracted response from JSON format into an ARRAY
    numpy_array = np.frombuffer(response_content_raw.encode('latin-1'), dtype=np.uint8)
    extra_elements = numpy_array.shape[0] - Desired_length
    print()
    print("Shape of DESERIALIZED JSON RESPONSE:", numpy_array.shape, "Extra Number of elements:", extra_elements)
    numpy_array = numpy_array[:-extra_elements]
    #numpy_array = numpy_array.reshape((Desired_height,Desired_width))
    numpy_array = numpy_array.reshape((Desired_width, Desired_height))
    print("Mask Shape for ARRAY made from POST respone", numpy_array.shape)

    # Create an image from the array
    predicted_mask = Image.fromarray(numpy_array, mode='L')
    # predicted_mask = Image.fromarray(numpy_array, mode='RGB')
    print("Mask Shape from REBUILDING the IMAGE using the POST respone ARRAY", predicted_mask.size)
    predicted_mask = image_to_base64(predicted_mask)

    # Convert the from in PIL.PngImagePlugin.PngImageFile format to a base64 string
    image = image_to_base64(image)

    mask = Image.open(mask_path)
    # Convert the mask from PIL.PngImagePlugin.PngImageFile format to a base64 string
    mask = image_to_base64(mask)

    # return send_from_directory("static", image_name, mimetype='image/png')
    return render_template("show_image.html", selected_picture=actual_pictures, image=image, mask=mask,
                           predicted_mask_path=predicted_mask)


# Closes the CONTEXT AFTER Python/SQL INTERACTION is completed
app_ctx.pop()

handler=Mangum(flask_web_app)

#if __name__ == '__main__':
#    flask_web_app.run(host='0.0.0.0', port=8000, debug=True)
