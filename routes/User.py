from flask import Blueprint,render_template,request,flash
from  uuid import uuid4
from database.database import db
from datetime import datetime


from flask_login import current_user,login_required

bp = Blueprint("user",__name__,url_prefix="/user")


from models.models import RoomMember,Room,User

@bp.route("/")
@login_required
def home():

    print(current_user.username)
    user_rooms = []
    user_rooms =  db.session.execute(
        db.select(Room)
        .join(Room.members)
        .filter_by(user_id=current_user.get_id())
    ).all()
    

    return render_template("user/home.html",user_rooms=user_rooms)



@bp.route("/create_room",methods=['GET','POST'])
@login_required
def create_room():

    if request.method == "POST":

        """
        
        1. Getting all the data from the form
        2. generating an UUID to identify the room
        3. creating a new instance of the room model
           and setting the current date and time.
        4. also setting the profesor_id, with the current_user
           the student_count is set to 1 because the profesor count as a individual member.
        5. after creating the room and inserting into the database we get the generated id from the room
        
        
        """
        room_title = request.form['room_title']
        room_description = request.form['room_description']
        room_code = uuid4().__str__()

        new_room  = Room(
            room_description=room_description,
            room_title=room_title,
            room_code=room_code,
            created_at_time=datetime.now().strftime("%H:%M:%S"),
            created_at_date=datetime.now().strftime("%Y-%m-%d"),
            student_count=1,
            profesor_id=current_user.get_id()
        )

        db.session.add(new_room)
        db.session.commit()

        #db.session.execute(db.select(User).filter_by(user_id=user_id)).first()[0]
        created_room = db.session.execute(db.select(Room).filter_by(room_code=room_code)).first()[0]
        
        new_room_member = RoomMember(
            user_id=current_user.get_id(),
            room_id=created_room.room_id
        )
        db.session.add(new_room_member)
        db.session.commit()
        flash("Successfully created!")
        


    return render_template("user/create_room.html")