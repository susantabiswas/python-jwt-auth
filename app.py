from auth.app import app, db

import argparse

def init_db():
    app.app_context().push()
    db.create_all()
    print('Database tables created...')

def remove_db():
    app.app_context().push()
    db.drop_all()
    print('Database tables deleted...')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-c", "--create", dest='command', action="store_const", const='create', help='Initialize database tables')
    group.add_argument("-d", "--drop", dest='command', action="store_const", const='drop', help='Delete all the database tables')
    group.add_argument("-s", "--server", dest='command', action="store_const", const='server', help='Start the flask server')
    
    args = parser.parse_args()

    if args.command == 'create':
        # Setup all the databases
        init_db()
    
    # Start flask server
    if args.command == 'server':
        app.run(
            debug=app.config['DEBUG'],
            host=app.config['HOST'],
            port=app.config['FLASK_PORT'])
    
    if args.command == 'drop':
        # remove all the databases
        remove_db()