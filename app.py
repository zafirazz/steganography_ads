from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from steg.aes import encrypt_message, decrypt_message
from steg.lsb import embed_message, extract_message
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle encode
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Only PNG images are supported.')
            return redirect(request.url)
        message = request.form.get('message', '')
        password = request.form.get('password', '')
        if not message or not password:
            flash('Message and password are required.')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)
        # Encrypt message
        encrypted = encrypt_message(message, password)
        # Embed
        output_path = os.path.join(RESULT_FOLDER, 'stego_' + filename)
        try:
            embed_message(input_path, encrypted, output_path)
        except Exception as e:
            flash(f'Error embedding message: {e}')
            return redirect(request.url)
        return send_file(output_path, as_attachment=True)
    return render_template('index.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Only PNG images are supported.')
            return redirect(request.url)
        password = request.form.get('password', '')
        if not password:
            flash('Password is required.')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)
        try:
            encrypted = extract_message(input_path)
            message = decrypt_message(encrypted, password)
        except Exception as e:
            flash(f'Error extracting or decrypting message: {e}')
            return redirect(request.url)
        return render_template('result.html', message=message)
    return render_template('decode.html')

if __name__ == '__main__':
    app.run(debug=True) 