from flask import Flask,render_template


from dotenv import load_dotenv
from database import db
from config  import Config

def create_app():


    app = Flask(__name__)
    
    load_dotenv()

    app.config.from_object(Config)

    db.init_app(app)

    @app.route("/",methods=['GET',"POST"])
    def index():
        return "<h1>Hello world </h1>"

    @app.route("/login",methods=['GET',"POST"])
    def login():
        return render_template("auth/login.html")

    @app.route("/register",methods=['GET',"POST"])
    def register():
        return render_template("auth/register.html")

    return app


app = create_app()
