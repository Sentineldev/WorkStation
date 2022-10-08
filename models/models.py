from sqlalchemy import ForeignKey
from database.database import db

class Person(db.Model):
        person_id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(20), nullable=False)
        last_name = db.Column(db.String(20), nullable=False)
        nationality = db.Column(db.String(30), nullable=False)
        birthdate = db.Column(db.DateTime, nullable=False)
        phones = db.relationship('Phone', backref= 'person', lazy= True)
        
        def __repr__(self) -> str:
            return f"{self.first_name} {self.last_name} - {self.person_id}"

class User(db.Model):
        user_id = db.Column(db.Integer, primary_key=True)
        person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
        username = db.Column(db.String(20), nullable=False)
        password = db.Column(db.String(30), nullable=False)
        
class Phone(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    phone_number = db.Column(db.String(15), primary_key=True)