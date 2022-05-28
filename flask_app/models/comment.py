from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import photo
from flask import flash



db = 'picture_this'
class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user_id']
        self.photo = data['photo_id']
        
    @classmethod
    def save_comment(cls, data):
        query = "INSERT INTO comments (comment, user_id, photo_id) VALUES (%(comment)s, %(user_id)s, %(photo_id)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_comments(cls):
        query= "SELECT * FROM comments;"
        results = connectToMySQL(db).query_db(query)
        comments = []
        # print(results)
        for row in results:
            comments.append( cls(row) )
        return comments

    @classmethod
    def validate_comment(self, comment):
        is_valid = True
        if not comment['comment']:
            is_valid = False
            flash("Must actually write something")
        return is_valid

    @classmethod
    def get_sender(cls, data):
        query = "SELECT * FROM comments JOIN users ON users.id = comments.user_id WHERE photo_id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        # print(results)
        comments = []
        for row in results:
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            user_instance = user.User(user_data)
            comment_data = {
                "id": row['id'],
                "comment": row['comment'],
                "user_id": row['user_id'],
                "photo_id": row['photo_id'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
                "user": user_instance
            }
            comment_instance = cls(comment_data)
            comments.append(comment_instance)
        return comments

#     @classmethod
#     def delete_comment(cls,data):
#         query = "DELETE FROM comments WHERE id = %(id)s;"
#         return connectToMySQL(db).query_db(query,data)

