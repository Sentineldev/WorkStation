from flask import Flask,url_for,redirect,session,render_template

from dotenv import load_dotenv
from config  import Config

from database.database import init_app

from routes import Auth

def create_app():


    app = Flask(__name__)
    

    #loading enviroment variables '.env file'.
    load_dotenv()


    """
    Configuration object
    DB Credentials and DB Engine
    
    """
    app.config.from_object(Config)


    #Connecting the ORM with the  flask app. ALSO adding the CLI command.
    init_app(app)


    app.register_blueprint(Auth.bp)


    @app.route("/",methods=['GET',"POST"])
    def index():


        return redirect(url_for('auth.login'))

    @app.route("/home",methods=['GET'])
    def home():
        user = session.get("current_user")
        return render_template("home/home.html",user=user)


    return app


app = create_app()