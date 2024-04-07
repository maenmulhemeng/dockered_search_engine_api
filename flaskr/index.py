import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, current_app
)


from flaskr.db import get_db,close_db,get_real_dict_cursor
import json

bp = Blueprint('index', __name__)
@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    #current_app.app_context().push()
   
    return render_template('index/index.html')

    
    
@bp.post('/search')
def search():
    searchQeury = request.form['searchQuery']
    try:
        db = get_db()
        cur = get_real_dict_cursor()
        y = json.dumps({"name":searchQeury})
        cur.execute("select doc_url,contents->>'id' as contents_id from docs where contents @> %s;", (y,))
        d = cur.fetchall()
        return d
    except Exception as e:
        error = repr(e)
        return error