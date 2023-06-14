import os

import cv2
from flask import Flask, render_template
from flask import request
from flask_cors import CORS
from werkzeug.utils import secure_filename

import detect

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = "static/images"


@app.route('/', methods=['GET'])
def get_index():
    return render_template('introduce.html')


@app.route('/upload', methods=['POST'] )
def predict_emotion():
    # Lấy hình ảnh xuống
    source = request.files['source']
    # Lấy tên hình ảnh
    filename = secure_filename(source.filename)
    source.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # địa chỉ chứa hình ảnh
    filename_input = "static/images/" + filename
    # Lấy về config
    opt = detect.detect(filename_input)
    image = detect.detect_face(opt)
    filename_result = 'static/images/result' + filename
    cv2.imwrite(filename_result, image)

    return render_template('introduce.html', img_old=filename,
                           img_rcn=filename_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6868')