from time import strftime
from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from database.database import db
from models.models import Post, Assignment
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