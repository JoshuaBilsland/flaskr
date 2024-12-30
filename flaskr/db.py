import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    """ Check if the connection has already been stored
    in the "g" object (global namespace).
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # open_resource() opens a file relative to the flaskr package
    # this is useful for when it is deployed as you won't know the location
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# Tells Python how to interpret timestamp values in the database
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


# close_db and init_db_command are registered with the application instance
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
