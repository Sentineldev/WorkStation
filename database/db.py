import mysql.connector as database
from utils import read_file
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
    """"""
    db = g.pop('db',None)
    if db is not None:
        db.close()


def init_db():
    """This function creates the tables for the database with a DDL code.
    
    Return: None
    """

    db, cursor = get_db()

    path = "/database/workstation_tables.sql"

    sql_ddl = read_file(path)

    try:
        cursor.execute(sql_ddl)
        db.commit()

    except Exception as ex:
        raise Exception(ex)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Command to invoke the init_db function.
    """
    init_db()
    click.echo("Successfully working...")

def init_app(app):
    """
    what this does is that after every query to any of the routes register in the app 
    will close the connection to the database.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)