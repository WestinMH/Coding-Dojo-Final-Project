from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import photo

db = 'picture_this'
class Like:
    def __init__(self, data):
        self.id = data['id']
        self.photo = data['photo_id']
        self.user = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # @classmethod
    # def get_likes(cls, data):
    #     query= "SELECT * FROM likes WHERE photo_id = %(id)s;"
    #     results = connectToMySQL(db).query_db(query, data)
    #     likes = []
    #     for row in results:
    #         likes.append( cls(row) )
    #     return likes

    # @classmethod
    # def get_sender(cls, data):
    #     query = "SELECT * FROM likes JOIN users ON users.id = likes.user_id WHERE photo_id = %(id)s;"
    #     results = connectToMySQL(db).query_db(query,data)
    #     print(results)
    #     likes = []
    #     for row in results:
    #         user_data = {
    #             "id": row['users.id'],
    #             "first_name": row['first_name'],
    #             "last_name": row['last_name'],
    #             "email": row['email'],
    #             "password": row['password'],
    #             "created_at": row['users.created_at'],
    #             "updated_at": row['users.updated_at']
    #         }
    #         user_instance = user.User(user_data)
    #         like_data = {
    #             "id": row['id'],
    #             # "sender_id": row['sender_id'],
    #             # "recipient_id": row['recipient_id'],
    #             "created_at": row['created_at'],
    #             "updated_at": row['updated_at'],
    #             "user": user_instance
    #         }
    #         like_instance = cls(like_data)
    #         likes.append(like_instance)
    #     return likes

    # @classmethod
    # def delete_like(cls,data):
    #     query = "DELETE FROM likes WHERE id = %(id)s;"
    #     return connectToMySQL(db).query_db(query,data)

    # @classmethod
    # def save_like(cls, data):
    #     query = "INSERT INTO likes ( user_id, photo_id) VALUES ( %(user_id)s, %(photo_id)s);"
    #     return connectToMySQL(db).query_db(query,data)
