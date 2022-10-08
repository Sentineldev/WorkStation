from flask import Flask,render_template

from dotenv import load_dotenv
from config  import Config

from database.database import init_app,db


from models.models import Person

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



    @app.route("/",methods=['GET',"POST"])
    def index():

        """
        
        TESTING THE ORM.
        
        """

        person = db.get_or_404(Person,1)
        print(person)
        return "<h1>Hello world </h1>"

    @app.route("/login",methods=['GET',"POST"])
    def login() -> str:
        """
        RETURNS HTML with a login screen.
        
        
        """

        return render_template("auth/login.html")

    @app.route("/register",methods=['GET',"POST"])
    def register() -> str:
        
        """
        RETURNS HTML with a register screen.
        
        """


        return render_template("auth/register.html")

    return app


app = create_app()