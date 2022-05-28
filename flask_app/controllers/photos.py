
from flask_app import app
from flask import flash, render_template,redirect,request, session
from flask_app.models import user
from flask_app.models import photo
from flask_app import app
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/westinhaugo/Documents/Coding projects/Final Project/flask_app/static/photos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/photos/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        flash('Must login or register!')
        return redirect('/')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect("/photos/upload")
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data  = {
            "title": request.form['title'],
            'description' : request.form['description'],
            "photo_path" : 'static/photos/'+filename,
            'photo_taken' : request.form['photo_taken'],
            'user_id' : session['user_id']
        }
        photo.Photo.save_photo(data)
        return redirect('/home')

@app.route('/photos/<int:id>')
def one_photo(id):
    if 'user_id' not in session:
        flash('Must login or register!')
        return redirect('/')
    return render_template('photo.html',
                            current_user = user.User.get_one({ "id" : session['user_id']}),
                            onePhoto = photo.Photo.get_one_photo({'id':id}),
                            user = user.User.get_one_user({'id': id})
                            )


@app.route('/photos/new')
def newphoto():
    if 'user_id' not in session:
        flash('Must login or register!')
        return redirect('/')
    return render_template('upload.html', current_user = user.User.get_one({ "id" : session['user_id']}))

@app.route('/delete_photo/<int:id>')
def deletephoto(id):
    if 'user_id' not in session:
        flash('Must login or register!')
        return redirect('/')
    data = {
        'id' : id
    }
    photo.Photo.delete_photo(data)
    return redirect('/home')
