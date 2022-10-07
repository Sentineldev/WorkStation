from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask.cli import with_appcontext
import click



db : SQLAlchemy = SQLAlchemy()



def init_db() -> None:

    """
    Create all the tables necessary to construct the database.
    
    """
    
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():

    """
    CALLBACK FUNCTION TO init the database.
    with the 'init-db' cli command.
    
    """

    init_db()
    click.echo("Hola mundo...")


def init_app(app: Flask) -> None:
    """
    
    Connect the ORM with the flask app.
    
    """

    db.init_app(app)
    app.cli.add_command(init_db_command)



