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

    if request.method == "POST":    

        #obtainng form data.
        username = request.form['username']
        password = request.form['password']

        name = request.form['name']
        last_name = request.form['last_name']
        country = request.form['country']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
        email = request.form['email']


        """
        Checking if the email and the username exists in the database.

        if not response message
        else 
        1. Create the person
        2. Querying to get the person auto generate id
        3. saving the phone along with the person's id
        4. created a new user along with the person's id

        also the password is save with a hash function
        
        """

        if Person.query.filter_by(email=email).first() is not None:
            flash("Email already exists")
        elif User.query.filter_by(username=username).first() is not None:
            flash("Username already exists")
        else:
            new_person = Person()
            new_person.first_name = name
            new_person.last_name = last_name
            new_person.country = country
            new_person.birthdate = birth_date
            new_person.email = email

            db.session.add(new_person)
            db.session.commit()

            addeed_person = Person.query.filter_by(email=email).first()
            
            new_phone = Phone()
            new_phone.person_id = addeed_person.person_id
            new_phone.phone_number = phone
            db.session.add(new_phone)
            db.session.commit()

            new_user = User()
            new_user.person_id = addeed_person.person_id
            new_user.username = username
            new_user.password = generate_password_hash(password)

            db.session.add(new_user)
            db.session.commit()

            flash("User registered successfully")

    return render_template("auth/register.html")






"""
closing the current session.

"""
@bp.route("/logout",methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))