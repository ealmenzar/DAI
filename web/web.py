from flask import Flask
from flask import render_template, request, session, url_for, redirect
import shelve
import pymongo
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

#print(conn)

db = conn.test

#cursor = db.restaurants.find()


#for doc in cursor:
   #print(doc)


@app.route('/')
def index():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, '/')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        return render_template('web.html', usuario=session['username'], pags=session['paginas'])
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
        return render_template('child.html', usuario=session['username'], pags=session['paginas'])
    return render_template('child.html')

@app.route('/Informacion')
def info():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'Informacion')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        return render_template('info.html', usuario=session['username'], pags=session['paginas'])
    return render_template('info.html')

@app.route('/Entradas')
def tickets():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'Entradas')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])
        return render_template('tickets.html', usuario=session['username'], pags=session['paginas'])
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
        if request.method == 'POST':
            data[u]['pass'] = request.form['password']
            data[u]['name'] = request.form['name']
            data[u]['lastname'] = request.form['lastname']
            data[u]['lastlastname'] = request.form['lastlastname']
            return render_template('profile.html', usuario=session['username'], pags=session['paginas'],
                                   pwd=data[u]['user'], name=data[u]['name'],
                                   lastname=data[u]['lastname'], lastlastname=data[u]['lastlastname'])

        return render_template('profile.html', usuario=session['username'], pags=session['paginas'],
                               pwd=data[u]['pass'], name=data[u]['name'],
                               lastname=data[u]['lastname'], lastlastname=data[u]['lastlastname'])
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

        return render_template('restaurantes.html', usuario=session['username'], pags=session['paginas'])
    return render_template('formulario.html')

@app.route('/AgregarRestaurante', methods=['GET', 'POST'])
def addrestaurant():
    if 'username' in session:
        s = session['paginas']
        s.insert(0, 'AgregarRestaurante')
        session['paginas'] = s
        if len(s) == 4:
            s.remove(s[3])

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
                   "grades": [
                   #    {"date": {"$date": 1393804800000}, "grade": "A", "score": 2},
                   #    {"date": {"$date": 1378857600000}, "grade": "A", "score": 6},
                   #    {"date": {"$date": 1358985600000}, "grade": "A", "score": 10},
                   #    {"date": {"$date": 1322006400000}, "grade": "A", "score": 9},
                   #    {"date": {"$date": 1299715200000}, "grade": "B", "score": 14}
                   ],
                   "name": name,
                   "restaurant_id": id
                   }
            db.restaurants.insert(dic)
            return render_template('agregarrestaurante.html', usuario=session['username'], pags=session['paginas'])
        return render_template('agregarrestaurante.html', usuario=session['username'], pags=session['paginas'])
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

        if request.method == 'POST':
            name = str(request.form['name'])
            barrio = str(request.form['barrio'])
            dic = {}
            if name != "":
                dic['name'] = name
            if barrio != "":
                dic['borough'] = barrio
            r = db.restaurants.find(dic)

            return render_template('buscarrestaurante.html', usuario=session['username'],
                                   pags=session['paginas'], restaurante=r)
        return render_template('buscarrestaurante.html', usuario=session['username'],
                               pags=session['paginas'])
    else:
        return render_template('formulario.html')



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__=='__main__':
    app.run(host='0.0.0.0')