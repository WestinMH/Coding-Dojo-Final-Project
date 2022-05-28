
from flask_app import app
from flask import flash, render_template,redirect,request, session
from flask_app.models import photo, comment, user
from flask_app import app
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

UPLOAD_DIRECTORY = '/Users/westinhaugo/Documents/Coding projects/Final Project/flask_app/static/avatars'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register_user', methods= ['POST'])
def submit():
    if not user.User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
        "confirm_password": request.form['confirm_password']
    }
    session['user_id'] = user.User.save(data)
    return redirect("/home")

@app.route ('/login_user', methods = ['POST'])
def loginUser():
    data = { "email" : request.form["email"]}
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/home')

@app.route('/home')
def photos():
    if 'user_id' not in session:
        flash('Must login or register!')
        return redirect('/')
    return render_template('home.html',
                            current_user=user.User.get_one({ "id" : session['user_id']}),
                            allPhotos = photo.Photo.get_photos(),
                            allUsers = photo.Photo.get_photos_with_users(),
                            allComments = comment.Comment.get_comments()
                            )

@app.route ('/users/edit/<int:id>')
def editUser(id):
    if 'user_id' not in session:
        flash('Must login or register!')
        return redirect('/')
    return render_template('edit_user.html',current_user = user.User.get_one({ "id" : id}))

@app.route ('/users/avatar/update', methods = ["GET", 'POST'])
def updateAvatar():
    if 'user_id' not in session:
        flash('Must login or register!')
        return redirect('/')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'avatar' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['avatar']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))
            print(filename)
        data  = {
            'user_id' : session['user_id'],
            "avatar": 'static/avatars/'+filename,
        }
        user.User.update_avatar(data)
        return redirect("/home")

@app.route ('/users/update/<int:id>', methods = ["GET", 'POST'])
def updateUser(id):
    if 'user_id' not in session:
        flash('Must login or register!')
        return redirect('/')
    if not user.User.validate_user(request.form):
        return redirect(f'/users/edit/{id}')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data  = {
        'id': id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user.User.update_user(data)
    return redirect('/home')


@app.route('/clear_session')
def clearSession():
    session.clear()
    return redirect('/')


