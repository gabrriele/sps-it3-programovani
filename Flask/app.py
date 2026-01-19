from flask import Flask, render_template, url_for, request
import os
import plotly.graph_objects as go
import plotly.io as pio

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

@app.route('/6', methods=['GET', 'POST']) #python => html
def prvniFormularCislo():
    result = None
    if request.method == 'POST':
        number = request.form.get('number', type=int) #přečti zadaný number z html
        if number is not None:
            result = number + 1 #přičti jedničku k číslu z html
    return render_template('index6.html', result=result)

# Cvičení 7
app.config["UPLOAD_FOLDER"] = "Flask/static/uploadedFiles/"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
@app.route('/7', methods=['GET', 'POST'])
def druhyFormular():
    content = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.txt'):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            file.seek(0)
            content = file.read().decode('utf-8')
    return render_template('index7.html', content=content)

# Cvičení 8
@app.route('/8')
def graph():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 20, 25, 30], mode='lines+markers', name='Data 1'))
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[15, 18, 22, 27], mode='lines+markers', name='Data 2'))
    fig.update_layout(
        title="Ukázkový interaktivní graf",
        xaxis_title="X-osa",
        yaxis_title="Y-osa",
        template="plotly_white"
    )
    # Převod grafu do HTML
    graph_html = pio.to_html(fig, full_html=False)
    return render_template("index8.html", graph_html=graph_html)


# Cvičení 8-2
@app.route('/8-2')
def graph82():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 20, 25, 30], mode='lines+markers', name='Data 1'))
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[15, 18, 22, 27], mode='lines+markers', name='Data 2'))
    fig.update_layout(
        title="Ukázkový interaktivní graf",
        xaxis_title="X-osa",
        yaxis_title="Y-osa",
        template="plotly_white"
    )
    # Převod grafu do HTML
    graph_html = pio.to_html(fig, full_html=False)
    return render_template("index8-2.html", graph_html=graph_html)