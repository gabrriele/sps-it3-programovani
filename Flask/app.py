from flask import Flask, render_template, url_for
app = Flask(__name__) #nazev pred route

@app.route('/')
def homes():
    return "Hello world!"

@app.route('/1')
def jednicka():
    return "Hello world!odjednicky"

@app.route('/2')
def pozdravZeSouboru():
    return render_template("index2.html") #html soubor = sablona podle ktere zpracuje (templates)

@app.route('/3')
def pozdravZeSouboruCSS():
    return render_template("index3.html")

@app.route('/4')
def pozdravZPromenne():
    text = "Ahoj z proměnné"
    return render_template("index4.html", message = text)

@app.route('/5')
def obrazek():
    image_url = url_for('static', filename='images/image.png')
    return render_template("index5.html", image_url = image_url)
