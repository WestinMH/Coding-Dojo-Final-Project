from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from flask import flash
from flask_app.models import photo

db = "picture_this"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$')

default_avatar = '/static/avatars/32-512-173841496.jpeg'
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.avatar = data['avatar']

    @classmethod
    def validate_user(self, user):
        is_valid = True
        if len(user['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 letters")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 letters")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address compilation")
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']): 
            flash("Invalid password compilation")
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

    @classmethod
    def validate_avatar(self, avatar):
        is_valid = True
        if not avatar['avatar']:
            is_valid = False
            flash("Must Include a Image File")
        return is_valid


    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update_avatar(cls, data):
        query = "UPDATE users SET avatar = %(avatar)s WHERE id = %(user_id)s"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row) )
        return users

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users JOIN photos ON users.id = photos.user_id WHERE photos.id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return results[0]

    @classmethod
    def get_one(cls,id):
        query  = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(db).query_db(query, id)
        return cls(result[0])

