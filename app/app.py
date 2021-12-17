import json
import mysql.connector
from flask_mysqldb import MySQL
from mysql.connector import Error,MySQLConnection
from flask import Flask,render_template,request,redirect,flash,url_for, session
import bcrypt

app = Flask(__name__)
app.secret_key = 'something_special'

app.config['MYSQL_HOST'] = 'www.db4free.net'
app.config['MYSQL_USER'] = 'fatima14'
app.config['MYSQL_PASSWORD'] = 'rachidfatima'
app.config['MYSQL_DB'] = 'dataflask'



mysql = MySQL(app)

def loadPosts():
    with open('post.json') as c:
        listOfPosts = json.load(c)['post']
        return listOfPosts

posts = loadPosts()

@app.route('/home',methods=['POST','GET'])
def home():
    if not session.get('logged_in'):
        flash('You must log to see this page')
        return render_template('login.html')
    return render_template('home.html', users=request.args.get('users'))

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == "POST":
        if request.form["email"] != '' and request.form["password"] != '':
            email = request.form['email']
            password = request.form['password']

            cur = mysql.connection.cursor()
            cur.execute("SELECT password from users where email = '"+ email+"' and password='" +password+"'")

            
            row = cur.fetchone()
            if row == None : 
                flash("Invalid username and password")
                return redirect(url_for("login"))  
            else:  
                        
                flash("Succesfully logged")
                session['logged_in'] = True
                return redirect(url_for('home'))      

        else:
            flash("Veuillez remplir les champs email et mot de passe", 'error')
            return redirect(url_for('login'))
       
    return render_template("login.html")

@app.route('/post')
def post():
    if not session.get('logged_in'):
        flash('You must log to see this page')
        return render_template('login.html')
    return render_template('welcome.html',posts = posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET' :
        return render_template("register.html")
    else:

        if(request.form['name'] != "" or request.form['email'] != "" or request.form['password'] != ""):
            name = request.form['name']
            email = request.form['email']
            password = request.form['password'].encode('utf_8')

            
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from users where email = '"+ email+"'")
            
            row = cur.fetchone()

            if row != None : 
                flash("Email existe déjà")
                return render_template("register.html")
            
            else:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(name,email,password,))
                mysql.connection.commit()

                flash("Votre compte a bien été créé, veuillez vous connecter")
                return redirect(url_for("login"))
        else:
            flash("Veuillez remplir tout les champs")
            return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('YOU HAVE SUCCESSFULLY LOGGED OFF!')
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)    