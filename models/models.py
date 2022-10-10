from enum import unique
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

    def __init__(self, first_name= None, last_name= None, country= None, 
                birthdate= None, email= None) -> None:
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.country = country
        self.birthdate = birthdate
        self.email = email
    
    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.person_id}"



class User(UserMixin,db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    username = db.Column(db.String(32), nullable=False,unique=True)
    password = db.Column(db.String(128), nullable=False)
    member_at = db.relationship('RoomMember', backref= 'user', lazy= True)

    def __init__(self, person_id= None, username= None, password= None) -> None:
        super().__init__()
        self.person_id = person_id
        self.username = username
        self.password = password
        
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
    
    def __init__(self, person_id= None, phone_number= None) -> None:
        super().__init__()
        self.person_id = person_id
        self.phone_number = phone_number

class Room(db.Model):
    room_id = db.Column(db.Integer, primary_key= True)
    room_code = db.Column(db.String(32), unique= True)
    room_title = db.Column(db.String(64), nullable= False)
    room_description = db.Column(db.String(512))
    student_count = db.Column(db.Integer)
    profesor_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    created_at_date = db.Column(db.Date, nullable= False)
    created_at_time = db.Column(db.Time, nullable= False)
    members = db.relationship('RoomMember', backref= 'room', lazy= True)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key= True)
    post_code = db.Column(db.String(32), unique= True)
    post_title = db.Column(db.String(64), nullable= False)
    post_description = db.Column(db.String(8192))
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
    created_at_date = db.Column(db.Date, nullable= False)
    created_at_time = db.Column(db.Time, nullable= False)

class Assignament(db.Model):
    assignament_id = db.Column(db.Integer, primary_key= True)
    assignament_code = db.Column(db.String(32), unique= True)
    assignament_title = db.Column(db.String(64), nullable= False)
    assignament_description = db.Column(db.String(8192))
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
    created_at_date = db.Column(db.Date, nullable= False)
    created_at_time = db.Column(db.Time, nullable= False)
    expiration_date = db.Column(db.Date, nullable= False)

class RoomMember(db.Model):
    room_member_id = db.Column(db.Integer, primary_key= True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))