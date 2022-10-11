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
    """"""
    if request.method == 'POST':
        
        # User data 
        username = request.form['username']
        password = request.form['password']
        
        # Person data
        name = request.form['name']
        last_name = request.form['last_name']
        email= request.form['email']
        country = request.form['country']
        birthdate = request.form['birth_date']
        
        # Phone number
        phone_number = request.form['phone']
        
        """We verify if the email or the username exists, if not exists then:
            
            1. We create a Person with the person data
            2. We query that person_id
            3. We create a User with the user data and the person_id
            4. We create a Phone with the phone number and the person_id
        """
        
        if db.session.execute(db.select(Person).filter_by(email=email)).first() is not None:
            flash("Email already registered!")
        elif db.session.execute(db.select(User).filter_by(username=username)).first() is not None:
            flash("Username already exists!")
        else:
            
            # Create the new person
            new_person = Person(
                first_name= name,
                last_name= last_name,
                birthdate= birthdate,
                country= country,
                email= email
            )
            
            db.session.add(new_person)
            db.session.commit()
            
            # We get the  person reciently created
            
            person_row = db.session.execute(db.select(Person).filter_by(email=email)).first()
            
            # Create the new user
            new_user = User(
                person_id= person_row.Person.person_id,
                username= username,
                password= generate_password_hash(password)
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            # Create the new phone
            new_phone = Phone(
                person_id= person_row.Person.person_id,
                phone_number= phone_number
            )
            
            db.session.add(new_phone)
            db.session.commit()
            
    return render_template("auth/register.html")






"""
closing the current session.

"""
@bp.route("/logout",methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))