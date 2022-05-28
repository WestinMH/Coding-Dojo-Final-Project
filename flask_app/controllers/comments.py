
from flask_app import app
from flask import redirect,request, session, render_template, flash
from flask_app.models import comment, photo, user
from flask_app import app


@app.route("/send_comment/<int:current_user_id>/<int:photo_id>", methods = ['GET', 'POST'])
def sendComment(current_user_id, photo_id):
    data = {
        "comment": request.form['comment'],
        "user_id" : current_user_id,
        "photo_id" : photo_id
    }
    if not comment.Comment.validate_comment(request.form):
        return redirect('/home')
    comment.Comment.save_comment(data)
    return redirect("/home")

@app.route('/delete_comment/<int:id>')
def deleteComment(id):
    data = {
        'id' : id
    }
    comment.Comment.delete_comment(data)
    return redirect('/home')