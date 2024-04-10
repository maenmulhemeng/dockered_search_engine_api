import os

from flaskr import db
from flask import Flask
from . import auth
from . import index
import threading
import requests
import json

def crawl(app,db,interval):
    threading.Timer(interval, crawl,[app,db, interval]).start()
    url = 'https://finances.worldbank.org/resource/zucq-nrc3.json'
    contents = requests.get(url)
    #print(len(contents.json()))
    with app.app_context():
        db1 = db.get_db()
        for c in contents.json():
            try:
                cur = db1.cursor()
                cur.execute(
                    'INSERT INTO docs (doc_url,contents) VALUES (%s, %s);',
                    (url, (json.dumps(c),)))               
                print(c["loan_number"])
            ###
            except db1.IntegrityError:
                error = f"doc_url {url} is already registered."
                pass
        db1.commit()
        print("Retrieve data")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    DB_HOST = os.environ.get("POSTGRES_HOST", None)
    DB_NAME = os.environ.get("POSTGRES_DB", None)
    DB_USER = os.environ.get("POSTGRES_USER", None)
    DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
    CRAWLER_RUN = True if os.environ.get("CRAWLER_RUN", None) == "yes" else False
    CRAWLER_INTERVAL = float(os.environ.get("CRAWLER_INTERVAL", None)) if CRAWLER_RUN else 0
    app.config.from_mapping(
        SECRET_KEY='dev',

        DATABASE=DB_NAME,
        HOST=DB_HOST,
        DB_USERNAME=DB_USER,
        DB_PASSWORD=DB_PASSWORD
    )

    db.init_app(app)

    print("Crawler will run" if CRAWLER_RUN else "No Crawler")
    if (CRAWLER_RUN == True):
        crawl(app,db, CRAWLER_INTERVAL)

    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    return app

