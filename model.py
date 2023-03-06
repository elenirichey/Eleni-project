"""Models for park playdates app"""

from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


# -------------------------------------------------------------------


class Region(db.Model):
    """A region"""

    __tablename__ = "regions"

    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region_name = db.Column(db.String(50), nullable=False, unique=True)
    state = db.Column(db.String(25), nullable=False)

    users=db.relationship("User", back_populates="region")
    parks = db.relationship("Park", back_populates="region")
    zipcodes = db.relationship("Zipcode", back_populates="region")
    messages = db.relationship("Message", back_populates="region")


    def __repr__(self):
        """Show info about region"""

        return f"region id = {self.region_id}, region name = {self.region_name}, region state = {self.state}>"
    



class User(db.Model):
    """A user """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(20), nullable = False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'), nullable=False)


    region= db.relationship("Region", back_populates="users")
    children = db.relationship("Child", back_populates="user")
    messages = db.relationship("Message", back_populates="user")


    def __repr__(self):
        """Show info about user"""

        return f"<user id = {self.user_id}, email = {self.email}, display name = {self.display_name}, Home Region ID = {self.region_id}>"

      


class Park(db.Model):
    """A park and/or playground"""

    __tablename__ = "parks"

    park_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    park_name = db.Column(db.String(50), nullable=False)
    park_address = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'), nullable=False)

    region = db.relationship("Region", back_populates="parks")
    messages = db.relationship("Message", back_populates="park")

    
    #do i also need a zipcode for parks -- search for parks in zipcode?

    def __repr__(self):
        """Show info about park"""

        return f"park id = {self.park_id}, park name = {self.park_name}, park region = {self.region_id}>"
    
    

class Zipcode(db.Model):
    """A zipcode"""

    __tablename__ = "zipcodes"

    zipcode = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'), nullable=False)

    region= db.relationship("Region", back_populates="zipcodes")

    def __repr__(self):
        """Show info about zipcode"""

        return f"zipcode = {self.zipcode}, region_id = {self.region_id}>"
    

class Child(db.Model):
    """age of a user's child""" 

    ___tablename__ = "children"

    child_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    birthdate = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship("User", back_populates="children")

    def __repr__(self):
        """Show info about child"""

        return f"Parent Id = {self.user_id}, birthdate = {self.birthdate}>"


class Message(db.Model):
    """a message posted to a message board"""

    __tablename__ = "messages"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable = False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'), nullable=False)
    message = db.Column (db.Text, nullable=False)
# ************* CHECK WHETHER ALL RELATIONSHIP TENSES WORK
    user=db.relationship("User", back_populates="messages")
    park=db.relationship("Park", back_populates="messages")
    region=db.relationship("Region", back_populates="messages") 
    """(region acts as the message board)"""

    def __repr__(self):
        """show info about message"""

        return f"message id = {self.post_id}, region id = {self.region_id}, user id = {self.user_id} time = {self.timestamp}>"
# <-- do i need to make this current/automatic // how
# timestamp before it gets to crud function 
#  how can i have them enter the birthday and get current age?? !!!


def connect_to_db(app, db_name = "Playdates"):
                  
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)
#

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print("connected to database")