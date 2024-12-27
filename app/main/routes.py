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
    my_files = File.query.filter_by(owner_id=current_user.id).all()
    access_files = current_user.access_files
    return render_template('index.html', users=users, my_files=my_files,
                           access_files=access_files)


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

            # добавляем access_users
            access_usernames = request.form.get('access_users')
            if access_usernames:
                access_users = access_usernames.split('\n')
                for username in access_users:
                    user = User.query.filter_by(username=username).first()
                    if user:
                        file_db.access_users.append(user)
                    else:
                        flash(f"User {username} not found")

            file.save(upload_path)
            db.session.commit()
            print(f"Время загрузки: {time.perf_counter() - start}")
            print(f"Время обработки запроса: {time.perf_counter() - post_time}")
            flash('File uploaded successfully')
            return redirect(url_for('main.info', uuid=file_db.uuid))
    return render_template('upload.html')


@main_bp.route('/info/<uuid>')
def info(uuid):
    file_db = File.query.get(uuid)
    if not file_db:
        flash('File not found')
    return render_template('file_info.html', file=file_db,
                           owner=current_user)


@main_bp.route('/download/<uuid>')
def download(uuid):
    file_db = File.query.get(uuid)
    if not file_db:
        flash('File not found')
        return redirect(url_for('main.index'))
    uploads = os.path.join(current_app.root_path, '..',
                           current_app.config['UPLOAD_FOLDER'])
    filename = f"{uuid}.{file_db.extension}"
    return send_from_directory(uploads, filename, as_attachment=True)
