from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import session, flash
import pprint

db = 'picture_this'

class Photo:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.photo_taken = data['photo_taken']
        self.photo_path = data['photo_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_photos(cls):
        query= "SELECT * FROM photos;"
        results = connectToMySQL(db).query_db(query)
        photos = []
        for row in results:
            photos.append( cls(row) )
        return photos

    @classmethod
    def get_one_photo(cls, data):
        query= "SELECT * FROM photos JOIN users ON users.id = photos.user_id WHERE photos.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_photos_with_users(cls,):
        query = "SELECT * FROM users LEFT JOIN photos on users.id = photos.user_id;"
        results = connectToMySQL(db).query_db(query)
        users=[]
        # pprint.pprint(results)
        for row in results:
            photo = {
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'photo_taken': row['photo_taken'],
                'photo_path': row['photo_path'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id']

            }
            users.append(cls(photo))
        return users

    @classmethod
    def delete_photo(cls,data):
        query = "DELETE FROM photos WHERE id = %(id)s ;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def save_photo(cls, data):
        query = "INSERT INTO photos (title, description, photo_taken, photo_path, user_id) VALUES (%(title)s, %(description)s,  %(photo_taken)s, %(photo_path)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def validate_photo(self, photo):
        is_valid = True
        print('hihihihihihihihihihi')
        print(len(photo['photo_path']))
        if len(photo['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 letters")
        # if len(photo['description']) < 3:
        #     is_valid = False
        #     flash("Description must be at least 10 characters")
        # if (photo['photo_path']) == None: 
        #     flash("Must include an image file")
        #     is_valid = False
        if photo['photo_taken'] == None:
            flash("Must include date")
            is_valid = False
        return is_valid
