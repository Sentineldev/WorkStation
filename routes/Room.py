from flask import Blueprint, render_template, request, flash,redirect,url_for
from flask_login import  login_required
from database.database import db
from models.models import AssignmentComment, Post, Assignment, Room, User,PostComment,Comment
from uuid import uuid4
from utils.validations import ValidateCreatePostForm, ValidateCreateAssignmentForm
from datetime import datetime


bp = Blueprint('room', __name__, url_prefix="/room")


@bp.route("/<actual_room_code>")
@login_required
def home(actual_room_code):
    """
    obtains all the post created in the current room 
    """
    room_parameters = {
        "posts": db.session.execute(
        db.select(Post)
        .filter_by(room_code=actual_room_code)
        ).all(),


        "assignments":db.session.execute(
            db.select(Assignment)
            .filter_by(room_code=actual_room_code)
        ).all(),

        "room":db.session.execute(
            db.select(Room)
            .filter_by(room_code=actual_room_code)
        ).first()[0],
    
        
        "room_code": actual_room_code}

    return render_template("room/home.html",room_parameters=room_parameters)


@bp.route("/<actual_room_code>/create_post", methods=['GET', 'POST'])
@login_required
def create_post(actual_room_code):
    """
    Create a new post to the actual room
    """

    if request.method == 'POST':

        """
        
        1. Getting all the data from the form
        2. Generating an UUID to identify the post
        3. Creating a new instance of the Post model
           and setting the current date and time.

        """

        form_validation = ValidateCreatePostForm(request.form)
        if form_validation["status"]:
            post_title = request.form['post_title']
            post_description = request.form['post_description']
            post_code = uuid4().__str__()

            new_post = Post(
                post_title= post_title,
                post_description= post_description,
                post_code= post_code,
                room_code= actual_room_code,
                created_at_time= datetime.now().strftime("%H:%M:%S"),
                created_at_date= datetime.now().strftime("%Y-%m-%d")
            )
        
            db.session.add(new_post)
            db.session.commit()

            flash("Post successfully created!")
            
        else:
            flash(form_validation["message"])

    return render_template("room/create_post.html", room_code=actual_room_code)


@bp.route("/<actual_room_code>/create_assignment", methods=['GET', 'POST'])
@login_required
def create_assignment(actual_room_code):

    """
    Create a new assignment to the actual room
    """

    if request.method == 'POST':

        """
        
        1. Getting all the data from the form
        2. Generating an UUID to identify the assignment
        3. Creating a new instance of the Assignment model
           and setting the current date and time.

        """

        form_validation = ValidateCreateAssignmentForm(request.form)
        if form_validation["status"]:
            assignment_title = request.form['assignment_title']
            assignment_description = request.form['assignment_description']
            assignment_ponderation = request.form['assignment_ponderation']
            expiration_date = request.form['expiration_date']
            assignment_code = uuid4().__str__()

            new_assignment = Assignment(
                assignment_title= assignment_title,
                assignment_description= assignment_description,
                assignment_code= assignment_code,
                assignment_ponderation= assignment_ponderation,
                room_code= actual_room_code,
                expiration_date= expiration_date,
                created_at_time= datetime.now().strftime("%H:%M:%S"),
                created_at_date= datetime.now().strftime("%Y-%m-%d")
            )
        
            db.session.add(new_assignment)
            db.session.commit()

            flash("Assignment successfully created!")
        else:
            flash(form_validation["message"])

    return render_template("room/create_assignment.html", room_code=actual_room_code)



@bp.route("/post/<post_code>",methods=['GET'])
@login_required
def post(post_code):

    """
    
    extracting data from the post with the current code
    including comments.    
    
    if any exception happens when extracting the  post data
    it will return the user to the home page.

    """

    try:
        post = db.session.execute(
            db.select(Post)
            .filter_by(post_code=post_code)
        ).first()

    except Exception as e:
        print(e)
        return redirect(url_for('user.home'))
    else:
        if post is None:
            return redirect(url_for('user.home'))
        return render_template("room/post.html",post=post[0])


@bp.route("/post/create_post_comment/<username>/<post_code>",methods=['POST'])
@login_required
def create_post_comment(username,post_code):


    """
    Checking that both user and post exists in the database
    then inserting the comment
    
    """

    comment_body = request.form['comment_body']
    
    #checking that the user exists

    if not  db.session.execute(db.select(User).filter_by(username=username)).first():
        flash("Error, user not found.")
    #checking that the post exists.
    elif not db.session.execute(db.select(Post).filter_by(post_code=post_code)).first():

        flash("Error, post not found.")
    #checking the length of the comment is correct.
    elif not (len(comment_body) > 0 and len(comment_body)<= 1024):
        flash("Comment must be between > 0 and <= 1024 characters")
    else:
        comment_code = uuid4().__str__()
        new_comment = Comment(
            comment_code=comment_code,
            comment_body=comment_body,
            created_at_time=datetime.now().strftime("%H:%M:%S"),
            created_at_date=datetime.now().strftime("%Y-%m-%d"),
            username=username
        )
        db.session.add(new_comment)
        db.session.commit()

        new_post_comment = PostComment(
            post_code=post_code,
            comment_code=comment_code
        )
        db.session.add(new_post_comment)
        db.session.commit()
    return redirect(url_for('room.post',post_code=post_code))


@bp.route("/assignment/<assignment_code>",methods=['GET'])
@login_required
def assignment(assignment_code):

    """
    view to show the assignment data.
    querying the db to get only the assignment with the given code.
    SINCE it's unique it will return the assignment or None.
    
    """

    try:
        assignment = db.session.execute(
            db.select(Assignment)
            .filter_by(assignment_code=assignment_code)
        ).first()

    except Exception as e:
        print(e)
        return redirect(url_for('user.home'))
    else:
        if post is None:
            return redirect(url_for('user.home'))
        return render_template("room/assignment.html",assignment=assignment[0])


@bp.route("/assignment/create_assignment_comment/<username>/<assignment_code>",methods=['POST'])
@login_required
def create_assignment_comment(username,assignment_code):


    """
    First we validated that the user and the assignment exists
    the comment format is correct.
    create the comment with the generated UUID
    and add to the relation table the current assignment and the new comment
    
    
    """

    comment_body = request.form['comment_body']

    if not  db.session.execute(db.select(User).filter_by(username=username)).first():
        flash("Error, user not found.")
    elif not  db.session.execute(db.select(Assignment).filter_by(assignment_code=assignment_code)).first():
        flash("Error, assignment not found.")
        
    elif not (len(comment_body) > 0 and len(comment_body)<= 1024):
        flash("Comment must be between > 0 and <= 1024 characters")
    else:
        comment_code = uuid4().__str__()

        new_comment = Comment(
            comment_code=comment_code,
            comment_body=comment_body,
            created_at_time=datetime.now().strftime("%H:%M:%S"),
            created_at_date=datetime.now().strftime("%Y-%m-%d"),
            username=username
        )
        db.session.add(new_comment)
        db.session.commit()
        new_assignment_comment = AssignmentComment(
            assignment_code = assignment_code,
            comment_code = comment_code
        )
        db.session.add(new_assignment_comment)
        db.session.commit()
    return redirect(url_for('room.assignment',assignment_code=assignment_code))