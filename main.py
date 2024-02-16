from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = os.path.join('uploads')
app.app_context().push()

class Files(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.Text(), nullable=False)
    fileurl = db.Column(db.Text(), nullable=False)
    filetype = db.Column(db.Text(), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, filename, fileurl, filetype):
        self.filename = filename
        self.fileurl = fileurl
        self.filetype = filetype

@app.route('/uploads/<path:filename>')
def send_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename)

@app.route('/')
def home():
    files = Files.query.all()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def uploadfiles():
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileurl = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
            new_file = Files(filename, fileurl, filename.split('.')[1])
            db.session.add(new_file)
            db.session.commit()
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
