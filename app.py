from flask import render_template, jsonify, Flask, redirect, url_for, request, make_response
import os
import io
import numpy as np
from PIL import Image
import keras.utils as image
from keras.models import model_from_json

app = Flask(__name__)

SKIN_CLASSES = {
    0: 'Actinic Keratosis (Solar Keratosis) or intraepithelial Carcinoma (Bowen’s disease)',
    1: 'Basal Cell Carcinoma',
    2: 'Benign Keratosis',
    3: 'Dermatofibroma',
    4: 'Melanoma',
    5: 'Melanocytic Nevi',
    6: 'Vascular skin lesion'

}


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/signin')
# def signin():
#     return render_template('signin.html')


# @app.route('/signup')
# def signup():
#     return render_template('signup.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

def desc(pred):
    if pred == 0:
        return "Actinic Keratosis is a skin condition caused by long-term exposure to ultraviolet (UV) radiation from the sun or artificial sources such as tanning beds. It typically appears as rough, scaly patches or lesions on sun-exposed areas of the skin, such as the face, scalp, ears, neck, backs of hands, and forearms."
    elif pred == 1:
        return "Basal cell carcinoma (BCC) is the most common type of skin cancer, typically developing in areas of the skin exposed to sunlight. It arises from the basal cells, which are found in the lower part of the epidermis, the outer layer of the skin."
    elif pred == 2:
        return "Benign Keratosis is a common non-cancerous skin growth that typically occurs in middle-aged or older adults. These growths are harmless and do not usually require treatment unless they become irritated or cosmetically undesirable."
    elif pred == 3:
        return "Dermatofibroma is a common benign skin lesion that typically appears as a small, firm, raised bump on the skin. These lesions can vary in color from pink to brown or red and often feel like hard nodules under the skin. Dermatofibromas usually develop on the arms or legs but can occur anywhere on the body."
    elif pred == 4:
        return "Melanoma is a type of skin cancer that originates in the melanocytes, the pigment-producing cells of the skin. It is the most serious form of skin cancer and can develop anywhere on the body, although it is most commonly found on areas exposed to the sun. Melanoma can also occur in areas that are not typically exposed to sunlight, such as the palms of the hands, soles of the feet, and under the nails."
    elif pred == 5:
        return "Melanocytic nevi, commonly referred to as moles, are benign growths on the skin that develop from melanocytes, the pigment-producing cells of the skin. They are typically brown or black in color and can vary in size, shape, and texture. Melanocytic nevi are common, with most people having multiple moles on their skin."
    elif pred == 6:
        return "Vascular skin lesions are abnormalities or growths on the skin that involve blood vessels. These lesions can vary in appearance, size, and color, depending on the specific type of vascular lesion."

def findMedicine(pred):
    if pred == 0:
        return "fluorouracil"
    elif pred == 1:
        return "Aldara"
    elif pred == 2:
        return "Hydrogen Peroxide (only when prescribed)"
    elif pred == 3:
        return "fluorouracil"
    elif pred == 4:
        return "fluorouracil (5-FU):"
    elif pred == 5:
        return "fluorouracil"
    elif pred == 6:
        return "fluorouracil"     
    
def notee(pred):
    if pred == 0:
        return "It is also recommended to take your doctor's Prescription for better results"
    elif pred == 1:
        return "It is also recommended to take your doctor's Prescription for better results"
    elif pred == 2:
        return "It is also recommended to take your doctor's Prescription for better results"
    elif pred == 3:
        return "It is also recommended to take your doctor's Prescription for better results"
    elif pred == 4:
        return "It is also recommended to take your doctor's Prescription for better results"
    elif pred == 5:
        return "It is also recommended to take your doctor's Prescription for better results"
    elif pred == 6:
        return "It is also recommended to take your doctor's Prescription for better results"        


@app.route('/detect', methods=['GET', 'POST'])
def detect():
    json_response = {}
    if request.method == 'POST':
        try:
            file = request.files['file']
        except KeyError:
            return make_response(jsonify({
                'error': 'No file part in the request',
                'code': 'FILE',
                'message': 'file is not valid'
            }), 400)

        imagePil = Image.open(io.BytesIO(file.read()))
        # Save the image to a BytesIO object
        imageBytesIO = io.BytesIO()
        imagePil.save(imageBytesIO, format='JPEG')
        imageBytesIO.seek(0)
        print("detected ")
        path = imageBytesIO
        j_file = open('model.json', 'r')
        loaded_json_model = j_file.read()
        j_file.close()
        model = model_from_json(loaded_json_model)
        model.load_weights('model.h5')
        img = image.load_img(path, target_size=(224, 224))
        img = np.array(img)
        img = img.reshape((1, 224, 224, 3))
        img = img/255
        prediction = model.predict(img)
        pred = np.argmax(prediction)
        disease = SKIN_CLASSES[pred]
        description = desc(pred)
        accuracy = prediction[0][pred]
        accuracy = round(accuracy*100, 2)
        medicine = findMedicine(pred)
        note = notee(pred)

        json_response = {
            "detected": False if pred == 2 else True,
            "disease": disease,
            "accuracy": accuracy,
            "description": description,
            "medicine" : medicine,
            "note" : note,
            "img_path": file.filename,

        }

        return make_response(jsonify(json_response), 200)

    else:
        return render_template('detect.html')


if __name__ == "__main__":
    app.run(debug=True, port=3000)
