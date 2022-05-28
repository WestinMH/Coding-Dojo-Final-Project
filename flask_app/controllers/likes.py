
from flask_app import app
from flask import flash, render_template,redirect,request, session
from flask_app.models import user
from flask_app.models import like
from flask_app import app

@app.route("/send_like/<int:current_user_id>/<int:photo_id>", methods = ['POST'])
def sendLike(current_user_id, photo_id):
    data = {
        "user_id" : current_user_id,
        "photo_id" : photo_id
    }
    like.Like.save_like(data)
    return redirect("/home")


# @app.route('/delete_like/<int:id>')
# def deletelike(id):
#     data = {
#         'id' : id
#     }
#     like.Like.delete_like(data)
#     return redirect('/home')