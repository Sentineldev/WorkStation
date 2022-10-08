from flask import Blueprint,render_template,request,flash


from database.database import db

bp = Blueprint("auth",__name__,url_prefix="/auth")


@bp.route("/login",methods=['GET','POST'])
def login():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        
        
    return render_template("auth/login.html")




@bp.route("/register",methods=['GET','POST'])
def register():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        name = request.form['name']
        last_name = request.form['last_name']
        country = request.form['country']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
    

    return render_template("auth/register.html")
