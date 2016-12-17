from flask import Flask
from flask import render_template, request, session, url_for, redirect
import shelve
import pymongo
import feedparser
#import tweepy
app = Flask(__name__)

app.debug = True
#usuarios = {}
data = shelve.open('data', writeback=True)
s = []

# Connection to Mongo DB
try:
    conn = pymongo.MongoClient()
    print("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB: %s" % e)

db = conn.test



@app.route('/')
def index():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, '/')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries
        return render_template('web.html', usuario=session['username'], pags=session['paginas'], news=news)
    return render_template('web.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ukey = str(request.form['username'])
        if ukey in data and data[ukey]['pass'] == request.form['password']:
            session['username'] = request.form['username']
            session['paginas'] = s
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Try again!'
            return render_template('web.html', error=error)
    return render_template('web.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        return render_template('formulario.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        ukey = str(request.form['username'])
        if ukey in data:
            error = 'Exists. Try again!'
            return render_template('formulario.html', error=error)
        else:
            ukey = str(request.form['username'])
            data[ukey] = {'user': ukey,
                          'pass': request.form['password'],
                          'name': request.form['name'],
                          'lastname': request.form['lastname'],
                          'lastlastname': request.form['lastlastname']}
            session['username'] = request.form['username']
            session['paginas'] = s
            return redirect(url_for('index'))
    return render_template('formulario.html')

@app.route('/Programacion')
def prog():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'Programacion')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries
        return render_template('child.html', usuario=session['username'], pags=session['paginas'], news=news)
    return render_template('child.html')

@app.route('/Informacion')
def info():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'Informacion')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries
        return render_template('info.html', usuario=session['username'], pags=session['paginas'], news=news)
    return render_template('info.html')

@app.route('/Entradas')
def tickets():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'Entradas')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries
        return render_template('tickets.html', usuario=session['username'], pags=session['paginas'], news=news)
    return render_template('tickets.html')

@app.route('/Perfil', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        u = str(session['username'])
        s = session['paginas']
        s.insert(0, 'Perfil')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries
        if request.method == 'POST':
            data[u]['pass'] = request.form['password']
            data[u]['name'] = request.form['name']
            data[u]['lastname'] = request.form['lastname']
            data[u]['lastlastname'] = request.form['lastlastname']
            return render_template('profile.html', usuario=session['username'], pags=session['paginas'],
                                   pwd=data[u]['user'], name=data[u]['name'],
                                   lastname=data[u]['lastname'], lastlastname=data[u]['lastlastname'], news=news)

        return render_template('profile.html', usuario=session['username'], pags=session['paginas'],
                               pwd=data[u]['pass'], name=data[u]['name'],
                               lastname=data[u]['lastname'], lastlastname=data[u]['lastlastname'], news=news)
    else:
        return render_template('formulario.html')

@app.route('/Restaurantes')
def restaurants():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'Restaurantes')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries
        return render_template('restaurantes.html', usuario=session['username'], pags=session['paginas'],news=news)
    return render_template('formulario.html')

@app.route('/AgregarRestaurante', methods=['GET', 'POST'])
def addrestaurant():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'AgregarRestaurante')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries

        if request.method == 'POST':
            building = int(request.form['building'])
            coord1 = float(request.form['coord1'])
            coord2 = float(request.form['coord2'])
            street = str(request.form['street'])
            zipcode = int(request.form['zipcode'])
            borough = str(request.form['borough'])
            cuisine = str(request.form['cuisine'])
            name = str(request.form['name'])
            id = int(request.form['id'])

            dic = {"address":
                       {"building": building,
                        "coord": [coord1, coord2],
                        "street": street,
                        "zipcode": zipcode},
                   "borough": borough,
                   "cuisine": cuisine,
                   "grades": [],
                   "name": name,
                   "restaurant_id": id
                   }
            db.restaurants.insert(dic)
            return render_template('agregarrestaurante.html', usuario=session['username'], pags=session['paginas'], news=news)
        return render_template('agregarrestaurante.html', usuario=session['username'], pags=session['paginas'], news=news)
    else:
        return render_template('formulario.html')

@app.route("/BuscarRestaurante", methods=['GET', 'POST'])
def buscarrestaurante():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'BuscarRestaurante')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries

        if request.method == 'POST':
            name = str(request.form['name'])
            r = db.restaurants.find({'name': name})
            coord = []
            rest = []
            for rr in r:
                coord.append([rr['address']['coord'][0], rr['address']['coord'][1]])
                rest.append([rr['name'], rr['cuisine'], rr['address']['street'], rr['borough']])

            return render_template('buscarrestaurante.html', usuario=session['username'],
                                   pags=session['paginas'], restaurante=rest, coord=coord, news=news)
        return render_template('buscarrestaurante.html', usuario=session['username'],
                               pags=session['paginas'], news=news)
    else:
        return render_template('formulario.html')

@app.route("/BorrarRestaurante/<pagina>", methods=['GET', 'POST'])
def borrarrestaurante(pagina):
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'BorrarRestaurante/20')
        session['paginas'] = s
        p = int(pagina)
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries

        r = db.restaurants.find()
        if request.method == 'POST':
            name = str(request.form['name'])
            dic = {"name": name}

            db.restaurants.remove(dic)
            r = db.restaurants.find()
            return render_template('borrarrestaurante.html', usuario=session['username'],
                                   pags=session['paginas'], r=r, pag=p, news=news)
        return render_template('borrarrestaurante.html', usuario=session['username'],
                               pags=session['paginas'], r=r, pag=p, news=news)
    else:
        return render_template('formulario.html')

@app.route("/Grafica")
def grafica():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'Grafica')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries

        brooklyn = db.restaurants.find({'borough': 'Brooklyn'})
        queens = db.restaurants.find({'borough': 'Queens'})
        staten = db.restaurants.find({'borough': 'Staten Island'})
        bronx = db.restaurants.find({'borough': 'Bronx'})
        manhattan = db.restaurants.find({'borough': 'Manhattan'})
        missing = db.restaurants.find({'borough': 'Missing'})

        nbrooklyn = brooklyn.count()
        nqueens = queens.count()
        nstaten = staten.count()
        nbronx = bronx.count()
        nmanhattan = manhattan.count()
        nmissing = missing.count()
        total = nbrooklyn + nqueens + nstaten + nbronx + nmanhattan + nmissing

        print(nstaten)

        dic = {'Brooklyn':nbrooklyn, 'Queens':nqueens, 'Staten':nstaten,
               'Bronx':nbronx, 'Manhattan':nmanhattan, 'Missing':nmissing, 'total': total}

        return render_template('grafica.html', usuario=session['username'],
                                   pags=session['paginas'], news=news, barrios=dic)
    else:
        return render_template('formulario.html')

@app.route('/Mapa')
def mapa():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'Mapa')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        rss_url = "http://www.binaural.es/feed/"
        feed = feedparser.parse(rss_url)
        news = feed.entries

        r = db.restaurants.find({ "grades.score": { '$gt': 60 } })
        rdic = []
        for rr in r:
            rdic.append([rr['address']['coord'][0], rr['address']['coord'][1]])

        return render_template('mapa.html', usuario=session['username'],
                               pags=session['paginas'], news=news, r=rdic)
    else:
        return render_template('formulario.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__=='__main__':
    app.run(host='0.0.0.0')

