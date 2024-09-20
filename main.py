from flask import Flask, jsonify, request, send_from_directory, make_response
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_extension = os.path.splitext(file.filename)[1]
    filename = str(uuid.uuid4()) + file_extension
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    download_link = f'/download/{filename}'
    return jsonify({'link': download_link})

@app.route('/download/<filename>')
def download_file(filename):
    response = make_response(send_from_directory(UPLOAD_FOLDER, filename))
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

if __name__ == '__main__':
    app.run(debug=True)