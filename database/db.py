import mysql.connector as database 
from flask import g,current_app
from flask.cli import with_appcontext

import click



def get_db():
    if 'db' not in g:
        g.db = database.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME']
        )
        g.c = g.db.cursor(dictionary=True)

        return g.db,g.c




def close_db(e=None):
    db = g.pop('db',None)
    if db is not None:
        db.close()




"""

INSERTS ALL THE TABLES to the database.

"""


def init_db():
    
    """
    Implementa la funcion para ejecutar inicializar la bd aqui
    
    """

    print("Funcionando")




"""

command to invoke the init_db function.

"""


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Successfully working...")




"""

what this does is that after every query to any of the routes register in the  app
will close the connection to the database.

"""
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)