from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return '''<html>
 
<head>
<title>El primer documento HTML</title>
<link rel="stylesheet" type="text/css" href="/static/css/style.css" media="screen" />
</head>
<body>


<p>Esto es <strong>LENGUAJE HTML</strong> </p>

</body> 

<img src="/static/imagenes/aprender-html.jpg" alt="IMAGEN" />

</html>'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
