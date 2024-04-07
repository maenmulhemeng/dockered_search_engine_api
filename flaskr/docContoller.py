from flask import Flask

app = Flask(__name__)

@app.get('/')
def doc_get():
    return []

@app.post('/login')
def login_post():
    # username = request.cookies.get('username')
    return do_the_login()
