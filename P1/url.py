from flask import Flask, abort
app = Flask(__name__)

# By default, a route answers to GET requests

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/user/pepe')
def hellopepe():
    return "Hello Pepe"

@app.route('/user/zerjillo')
def hellozerjillo():
    return "Hello Zerjillo"

@app.route('/user/<username>')
def hellouser(username):
    return "Hello %s" % username

@app.errorhandler(404)
def error(error):
    return "Pagina no encontrada", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')