from database.database import db

from flask_login import UserMixin

class Person(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(32), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(128),unique=True, nullable=False)
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
    person_email = db.Column(db.String(128), db.ForeignKey('person.email'))
    username = db.Column(db.String(32), nullable=False,unique=True)
    password = db.Column(db.String(128), nullable=False)
    member_at = db.relationship('RoomMember', backref= 'user', lazy= True)
    comment = db.relationship("Comment",backref='user',lazy=True)

    def __init__(self, person_email= None, username= None, password= None) -> None:
        super().__init__()
        self.person_email = person_email
        self.username = username
        self.password = password
        
    def __repr__(self) -> str:
        return f"{self.username} {self.user_id}"



    """
    Override of the UserMxin method get_id  
    """
    def get_id(self) -> int:
        return self.user_id
        
class Phone(db.Model):
    person_email = db.Column(db.String(128), db.ForeignKey('person.email'))
    phone_number = db.Column(db.String(16), primary_key=True)
    
    def __init__(self, person_email= None, phone_number= None) -> None:
        super().__init__()
        self.person_email = person_email
        self.phone_number = phone_number

class Room(db.Model):
    room_id = db.Column(db.Integer, primary_key= True)
    room_code = db.Column(db.String(36), unique= True,nullable=False)
    room_title = db.Column(db.String(64), nullable= False)
    room_description = db.Column(db.String(512))
    student_count = db.Column(db.Integer)
    profesor_email = db.Column(db.String(128), db.ForeignKey('person.email'))
    created_at_date = db.Column(db.Date, nullable= False)
    created_at_time = db.Column(db.Time, nullable= False)
    members = db.relationship('RoomMember', backref= 'room', lazy= True)


class RoomMember(db.Model):
    room_member_id = db.Column(db.Integer, primary_key= True)
    room_code = db.Column(db.String(36), db.ForeignKey('room.room_code'))
    username = db.Column(db.String(32), db.ForeignKey('user.username'))

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key= True)
    post_code = db.Column(db.String(36), unique= True)
    post_title = db.Column(db.String(64), nullable= False)
    post_description = db.Column(db.String(8192), nullable= False)
    room_code = db.Column(db.String(36), db.ForeignKey('room.room_code'))
    created_at_date = db.Column(db.Date, nullable= False)
    created_at_time = db.Column(db.Time, nullable= False)
    comments = db.relationship('PostComment', backref= 'post', lazy= True)



class Assignment(db.Model):
    assignment_id = db.Column(db.Integer, primary_key= True)
    assignment_code = db.Column(db.String(36), unique= True)
    assignment_title = db.Column(db.String(64), nullable= False)
    assignment_description = db.Column(db.String(8192))
    assignment_ponderation = db.Column(db.Integer, nullable=False)
    room_code = db.Column(db.String(36), db.ForeignKey('room.room_code'))
    created_at_date = db.Column(db.Date, nullable= False)
    created_at_time = db.Column(db.Time, nullable= False)
    expiration_date = db.Column(db.Date, nullable= False)

    comments = db.relationship('AssignmentComment', backref= 'assignment', lazy= True)



class Comment(db.Model):
    comment_id = db.Column(db.Integer,primary_key=True)
    comment_code = db.Column(db.String(36),nullable=False,unique=True) 
    comment_body = db.Column(db.String(1024),nullable=False)
    username = db.Column(db.String(32),db.ForeignKey('user.username'))
    created_at_date =  db.Column(db.Date,nullable=False)
    created_at_time = db.Column(db.Time,nullable=False)

    comments_at_post = db.relationship('PostComment', backref= 'comment', lazy= True)
    comments_at_assignment = db.relationship('AssignmentComment', backref= 'comment', lazy= True)



class PostComment(db.Model):
    post_comment_id = db.Column(db.Integer,primary_key=True)
    post_code = db.Column(db.String(36),db.ForeignKey('post.post_code'))
    comment_code = db.Column(db.String(36),db.ForeignKey('comment.comment_code'))


class AssignmentComment(db.Model):
    assignment_comment_id = db.Column(db.Integer,primary_key=True)
    assignment_code = db.Column(db.String(36),db.ForeignKey('assignment.assignment_code'))
    comment_code = db.Column(db.String(36),db.ForeignKey('comment.comment_code'))




