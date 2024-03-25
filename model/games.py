""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Game(db.Model):
    __tablename__ = 'games'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _gameid = db.Column(db.String(255), unique=True, nullable=False)
    _genre = db.Column(db.String(255), unique=False, nullable=False)
    _rating = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    ##posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, gameid, genre = "basic", rating = "1"):
        self._name = name    # variables with self prefix become part of the object, 
        self._gameid = gameid
        self._genre = genre
        self._rating = rating


    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def genre(self):
        return self._genre
    
    @genre.setter
    def genre(self, genre):
        self._genre = genre
    
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, rating):
        self._rating = rating
    
    # a getter method, extracts email from object
    @property
    def gameid(self):
        return self._gameid
    
    # a setter function, allows name to be updated after initial object creation
    @gameid.setter
    def gameid(self, gameid):
        self._gameid = gameid
        
    # check if uid parameter matches user id in object, return boolean
    def is_gameid(self, gameid):
        return self._gameid == gameid
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "gameid": self.gameid,
            "genre": self.genre,
            "rating": self.rating
            # "posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", gameid="",rating=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(gameid) > 0:
            self.uid = gameid
        if len(rating) > 0:
            self.rating = rating
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initGames():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = Game(name='Tommy boy', gameid='tommy',  genre="numnums", rating="1")
        u2 = Game(name='Nick Her', gameid='niko', genre="electricity", rating="1")
        u3 = Game(name='Alexi', gameid='A-Rod',  ganre="User", rating="1")
        u4 = Game(name='Simba Lion', gameid='simba', genre="User", rating="1")
        u5 = Game(name='Sai Talisetty', gameid='sai', password='123sai', dob=date(2008, 6, 9), hashmap={"job": "football player", "company": "Seattle Seahawks"}, food="Annie's bunny gummies", favorite="1")

        games = [u1, u2, u3, u4, u5]

        """Builds sample user/note(s) data"""
        for game in games:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 5)):
                    note = "#### " + game.name + " note " + str(num) + ". \n Generated by test data."
                    '''user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))'''
                '''add user/post data to table'''
                game.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {game.uid}")
            