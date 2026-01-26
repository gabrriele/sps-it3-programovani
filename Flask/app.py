from flask import Flask, render_template, url_for, request, redirect, session
import os
import plotly.graph_objects as go
import plotly.io as pio
import bcrypt
import mysql.connector
from pripojeni5 import *
app = Flask(__name__) #nazev pred route

app.secret_key = "nizkyKlic"

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


# Cvičení 9
@app.route('/9/<int:id>/<string:name>', methods = ['GET'])
def parametry(id, name):
    return render_template("index9.html", id=id, name=name)


#Cvičení 10
@app.route('/10', methods=['GET', 'POST'])
def redirekting():
    result = None
    if request.method == 'POST':
        number = request.form.get('number', type=int)
        result = number
        if number == 1:
            return redirect('/1')
        elif number ==2:
            return redirect('/2')
        else:
            return render_template("index10.html", result=result)
        
    else:
        return render_template("index10.html", result=result)
    


#Home
@app.route('/home')
def home_login_ukazka():
    return render_template('formular/home.html', email=session.get('email'))


#Logout
@app.route('/logout')
def logout():
    # Odstranění uživatele ze session
    session.pop('email', None)
    return redirect(url_for('home'))


#Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['jmeno']
        mail = request.form['email']
        psw = request.form['psw']
        
        hashed_password = bcrypt.hashpw(psw.encode('utf-8'), bcrypt.gensalt())
        hesloDoDB = hashed_password.decode('utf-8')
        mydb = mysql.connector.connect(
        host = HOST
        ,user = USER
        ,password = PASSWORD
        ,database = DATABASE
        )
        
        mycursor = mydb.cursor()
        # Create the Pojišťovny table
        mycursor.execute("""CREATE TABLE IF NOT EXISTS uzivatele
        (
            id int AUTO_INCREMENT PRIMARY KEY,
            jmeno varchar(35) NOT NULL,
            email varchar(50) NOT NULL,
            heslo varchar(255) NOT NULL
        );""")
        mydb.commit()


        sql = "INSERT INTO uzivatele (jmeno, email, heslo) VALUES (%s, %s, %s)"
        values = (name, mail, hesloDoDB)
        mycursor.execute(sql, values)
        mydb.commit()


        return redirect(url_for('login'))
    return render_template("formular/register.html")


#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']

        mydb = mysql.connector.connect(
            host = HOST
        ,user = USER
        ,password = PASSWORD
        ,database = DATABASE
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT heslo FROM uzivatele WHERE email = %s;", (email,))
        result = mycursor.fetchone()

        if result:
            stored_hashed_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                session['email'] = email
                return redirect(url_for('home'))
            else:
                error_message = "Invalid email or password."
        else:
            error_message = "User not found."

        return render_template("formular/login.html", error=error_message)
    return render_template("formular/login.html")


#Tabulka
@app.route('/tabulka')
def tabulka():
    if 'email' not in session:
        # Pokud uživatel není přihlášený, přesměrujeme ho na login
        return redirect(url_for('login'))
    elif 'email' in session:
        mydb = mysql.connector.connect(
            host = HOST
            ,user = USER
            ,password = PASSWORD
            ,database = DATABASE
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM uzivatele")
        result = mycursor.fetchall()
        
        return render_template("formular/tabulka.html", email=session.get('email'), items = result)









if __name__ == '__main__':
    app.run()