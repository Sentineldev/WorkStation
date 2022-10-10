from flask import Blueprint,render_template,request,flash,redirect,url_for

from flask_login import login_user,logout_user,current_user
from werkzeug.security import check_password_hash,generate_password_hash

from database.database import db

from models.models import User,Person,Phone

bp = Blueprint("auth",__name__,url_prefix="/auth")


@bp.route("/login",methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        #obtaining form data.
        username = request.form['username']
        password = request.form['password'] 

        """
        First querying a row from the database with the given credentials
        logging the user if the credentials match with any row in the db.
        
        """
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("Wrong credentials")
        elif not check_password_hash(user.password,password) : #checking if the hashed password matches with the password
            flash("Wrong credentials")
        else:
            """
            login user.
            """
            login_user(user)
            return redirect(url_for('home')) 
        
        
    return render_template("auth/login.html")




@bp.route("/register",methods=['GET','POST'])
def register():


            

    return render_template("auth/register.html")






"""
closing the current session.

"""
@bp.route("/logout",methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))