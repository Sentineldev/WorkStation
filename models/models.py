from database.database import db
from uuid import uuid3

from flask_login import UserMixin

class Person(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(32), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(128),unique=True)
    phones = db.relationship('Phone', backref= 'person', lazy= True)

        
    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.person_id}"



class User(UserMixin,db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    username = db.Column(db.String(32), nullable=False,unique=True)
    password = db.Column(db.String(128), nullable=False)


    def __repr__(self) -> str:
        return f"{self.username} {self.user_id}"

    def toDict(self) -> dict:
        return {
            "username":self.username,
            "user_id":self.user_id,
            "person_id":self.person_id
        }


    """
    Override of the UserMxin method get_id  
    """
    def get_id(self) -> int:
        return self.user_id
        
class Phone(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    phone_number = db.Column(db.String(16), primary_key=True)

class Room(db.Model):
    room_id = db.Column(db.Integer, primary_key= True)
    room_title = db.Column(db.String(64), nullable= False)
    room_description = db.Column(db.String(512))
    student_count = db.Column(db.Integer)
    profesor_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    created_at_date = db.Column(db.Date, nullable= False)
    created_at_time = db.Column(db.Time, nullable= False)
    posts = db.relationship('Post', backref= 'room', lazy= True)
    assignaments = db.relationship('Assignament', backref= 'room', lazy= True)
    registered_students = db.relationship('Registered', backref= 'room', lazy= True)

class Post(db.Model):
	post_id = db.Column(db.Integer, primary_key= True)
	post_title = db.Column(db.String(64), nullable= False)
	post_description = db.Column(db.String(8192))
	room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
	created_at_date = db.Column(db.Date, nullable= False)
	created_at_time = db.Column(db.Time, nullable= False)

class Assignament(db.Model):
    assignament_id = db.Column(db.Integer, primary_key= True)
    assignament_title = db.Column(db.String(64), nullable= False)
    assignament_description = db.Column(db.String(8192))
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
    created_at_date = db.Column(db.Date, nullable= False)
    created_at_time = db.Column(db.Time, nullable= False)
    expiration_date = db.Column(db.Date, nullable= False)

class Registered(db.Model):
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))