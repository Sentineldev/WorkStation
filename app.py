from distutils.log import debug
from flask import Flask


from dotenv import load_dotenv
from database import db
from config  import Config

def create_app():


    app = Flask(__name__)
    
    load_dotenv()

    app.config.from_object(Config)

    db.init_app(app)



    return app


app = create_app()