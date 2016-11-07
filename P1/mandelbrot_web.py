from flask import Flask
from flask import request, redirect, url_for
from PIL import Image

app = Flask(__name__)
app.debug = True


def renderizaMandelbrotBonito(x1, y1, x2, y2, ancho, iteraciones, nombreFicheroPNG, paleta, nColoresPaleta):
    # drawing area
    xa = x1
    xb = x2
    ya = y1 + 0.000001
    yb = y2
    maxIt = iteraciones
    # image size
    imgx = ancho
    imgy = int(abs(y2 - y1) * ancho / abs(x2 - x1));

    image = Image.new("RGB", (imgx, imgy))

    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1) + ya
        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1) + xa
            z = zx + zy * 1j
            c = z
            for i in range(maxIt):
                if abs(z) > 2.0: break
                z = z * z + c

            if (i == maxIt - 1):
                image.putpixel((x, y), (0, 0, 0))  # El nucleo del fractal en negro
            else:
                image.putpixel((x, y), getColorPaleta(paleta, nColoresPaleta, i))

    image.save(nombreFicheroPNG, "PNG")

def getColorPaleta(paleta, nColoresPaleta, color):
    nuevoColor = color % (nColoresPaleta)

    nPuntosControlPaleta = len(paleta)

    icolor1 = float(nuevoColor) * float(nPuntosControlPaleta - 1) / float(nColoresPaleta - 1)

    # print len(paleta)
    # print int(icolor1)

    if (int(icolor1) == len(paleta) - 1):  # Devolvemos el ultimo color
        return paleta[len(paleta) - 1]

    porcentajeC2 = icolor1 - int(icolor1)
    porcentajeC1 = 1.0 - porcentajeC2
    icolor1 = int(icolor1)
    icolor2 = icolor1 + 1

    nr = int(paleta[icolor1][0] * porcentajeC1 + paleta[icolor2][0] * porcentajeC2)
    ng = int(paleta[icolor1][1] * porcentajeC1 + paleta[icolor2][1] * porcentajeC2)
    nb = int(paleta[icolor1][2] * porcentajeC1 + paleta[icolor2][2] * porcentajeC2)

    return (nr, ng, nb)


@app.route("/mandelbrot", methods=['GET'])
def mandelbrot():
    x1 = float(request.args.get('x1'))
    y1 = float(request.args.get('y1'))
    x2 = float(request.args.get('x2'))
    y2 = float(request.args.get('y2'))
    ancho = int(request.args.get('ancho'))

    a = int(request.args.get('paleta1a'))
    b = int(request.args.get('paleta1b'))
    c = int(request.args.get('paleta1c'))
    l1 = (a, b, c)
    a = int(request.args.get('paleta2a'))
    b = int(request.args.get('paleta2b'))
    c = int(request.args.get('paleta2c'))
    l2 = (a, b, c)
    a = int(request.args.get('paleta3a'))
    b = int(request.args.get('paleta3b'))
    c = int(request.args.get('paleta3c'))
    l3 = (a, b, c)
    paleta = [l1, l2, l3]

    ncolores = int(request.args.get('ncolores'))
    iteraciones = 100
    renderizaMandelbrotBonito(x1,y1,x2,y2,ancho,iteraciones, "static/imagenes/mandelbrot_web.png", paleta, ncolores)

    return '''
    <h1>MANDELBROT</h1>
    <img src="static/imagenes/mandelbrot_web.png"></img>
    '''

# http://localhost:8080/mandelbrot?x1=-1&y1=-1&x2=1&y2=1&ancho=300&paleta1a=255&paleta1b=0&paleta1c=0&paleta2a=0&paleta2b=255&paleta2c=0&paleta3a=0&paleta3b=0&paleta3c=255&ncolores=10

if __name__ == "__main__":
    app.run(host='0.0.0.0')
