from flask import Flask
from flask import render_template, request, session, url_for, redirect
import shelve
app = Flask(__name__)

app.debug = True
#usuarios = {}
data = shelve.open('data', writeback=True)
s = []

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


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__=='__main__':
    app.run(host='0.0.0.0')