from flask import Flask,url_for,redirect,render_template

from dotenv import load_dotenv
from config  import Config




from flask_login import  login_required


from database import database
import login_manager

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
    database.init_app(app)
    login_manager.init_app(app)


    app.register_blueprint(Auth.bp)


    @app.route("/",methods=['GET',"POST"])
    def index():


        return redirect(url_for('auth.login'))


    """
    TESTING login_required decorator.
    
    """

    @app.route("/home",methods=['GET'])
    @login_required
    def home():
        return render_template("home/home.html")


    return app


app = create_app()