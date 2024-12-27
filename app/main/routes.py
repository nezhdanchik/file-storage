import os
import time
from time import perf_counter

from flask import render_template, request, flash, redirect, url_for, \
    current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import main_bp
from ..models import User, File
from .. import cache, db


@main_bp.route('/')
@login_required
@cache.cached(timeout=60)
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        post_time = perf_counter()
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            start = time.perf_counter()
            # filename = secure_filename(file.filename)
            filename = file.filename
            extension = filename.rsplit('.', 1)[1].lower()
            file_db = File(filename=filename, owner_id=current_user.id,
                           extension=extension)
            db.session.add(file_db)
            db.session.flush()

            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                       f"{file_db.uuid}.{extension}")
            file.save(upload_path)
            db.session.commit()
            print(f"Время загрузки: {time.perf_counter() - start}")
            print(f"Время обработки запроса: {time.perf_counter() - post_time}")
            flash('File uploaded successfully')
            return render_template('file_info.html', file=file_db,
                                   owner=current_user)
    return render_template('upload.html')


@main_bp.route('/download/<uuid>')
def download(uuid):
    file_db = File.query.get(uuid)
    if not file_db:
        flash('File not found')
        return redirect(url_for('main.index'))
    uploads = os.path.join(current_app.root_path, '..',
                           current_app.config['UPLOAD_FOLDER'])
    filename = f"{uuid}.{file_db.extension}"

    file_path = os.path.join(uploads, f"{uuid}.{file_db.extension}")
    print(f"Attempting to fetch file from: {file_path}")
    if not os.path.exists(file_path):
        print("File does not exist at specified path")


    return send_from_directory(uploads, filename, as_attachment=True)


@main_bp.route('/hi/<uuid>')
def hi(uuid):
    flash(f'Hi, {uuid}')
    return render_template('base.html')
