import os
from flask import render_template, redirect, request, url_for, send_from_directory, abort
from app import app
from werkzeug.utils import secure_filename
from flask import send_from_directory

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

import imghdr

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_PATH_2'] = '../uploads'

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/upload_file')
def upload_index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('upload_files.html', files=files)

@app.route('/upload_file', methods=['POST'])
def upload_files():
    if "SubmitBtn" in request.form:
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return redirect(url_for('upload_files'))
    if "GenerateBtn" in request.form:
        return redirect(url_for('index'))
    


@app.route('/upload/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH_2'], filename) 
