from flask import Flask, Response, request, jsonify, redirect, url_for, render_template
from werkzeug.utils import secure_filename  
from tensorflow.keras.models import load_model
import numpy as np
import os
import cv2 


# Some constants to be used in the model
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMG_SIZE = (32,32)

# Character mapping of the model
char_map = {
    0:'𑑐(0)',   1:'𑑑(1)',    2:'𑑒(2)',   3:'𑑓(3)',      4: '𑑔(4)',     5: '𑑕(5)',    6: '𑑖(6)',    7: '𑑗(7)',
    8:'𑑘(8)',   9:'𑑙(9)',    10:'𑑉(OM)', 11:'𑐀(A)',    12: '𑐁(AA)',   13: '𑐀𑑅(AH)',  14: '𑐂(I)',    
    15:'𑐃(II)',16:'𑐄(U)',   17:'𑐅(UU)',  18:'𑐆(R)',    19: '𑐆𑐺(RR)',  20: '𑐊(E)',   21: '𑐋(AI)',    22: '𑐌(O)',    
    23:'𑐍(AU)', 24:'𑐈(L)',  25:'𑐉(LL)',   26:'𑐎(KA)',   27: '𑐎𑑂𑐳(KSA)', 28: '𑐏(KHA)',29: '𑐐(GA)',    30: '𑐑(GHA)',    
    31:'𑐒(NGA)',32:'𑐔(CA)',  33:'𑐕(CHA)', 34:'𑐖(JA)',   35: '𑐖𑑂𑐘(JñA)',  36: '𑐗(JHA)',37: '𑐗(JHA-alt)',38: '𑐘(NYA)',    
    39:'𑐚(TA)', 40:'𑐛(TTHA)', 41:'𑐜(DDA)', 42:'𑐝(DHA)',  43: '𑐞(NNA)', 44: '𑐟(TA)',  45: '𑐟𑑂𑐬(TRA)',    46: '𑐠(THA)',
    47:'𑐡(DA)', 49:'𑐣(NA)',   50:'𑐥(PA)',  51:'𑐦(PHA)',  52: '𑐧(BA)',  53: '𑐨(BHA)',  54: '𑐩(MA)',    55: '𑐫(YA)', 
    56:'𑐬(RA)', 57: '𑐮(LA)', 58:'𑐰(WA)', 59:'𑐱(SHA)',    60: '𑐱(SHA-alt)', 61: '𑐲(SSA)',    62: '𑐳(SA)', 63: '𑐴(HA)'
}

# Loading the model here
model = load_model('vgg.h5')

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function for predicting the model
def predict(image_path):
    image = cv2.imread(image_path, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(np.array(image), IMG_SIZE)
    image = image.astype('float32')
    image = np.expand_dims(image, axis=0)

    output = model.predict(image)
    result = char_map[np.argmax(output)]
    
    return result

# Defining the app here
app = Flask(__name__)


# Routes defined here
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = UPLOAD_FOLDER + '/' + filename
        file.save(file_path)
        
        # Prediction goes here
        predicted_class = predict(file_path)
        
        return jsonify({'predicted_class': predicted_class})
    
    return jsonify({'error': 'Invalid file format'})

@app.route('/test')
def test():
    return jsonify({'message': 'the server is running very well'})

if __name__ == "__main__":
    app.run(debug=True)