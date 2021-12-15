import json
import pymysql.cursors
from flask import Flask,render_template,request,redirect,flash,url_for, session

def loadUsers():
    with open('users.json') as c:
         listOfUsers = json.load(c)['users']
         return listOfUsers

def loadPosts():
    with open('post.json') as c:
        listOfPosts = json.load(c)['post']
        return listOfPosts

app = Flask(__name__)
app.secret_key = 'something_special'

users = loadUsers()
user = None
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
            try : 
                user = [user for user in users if user['email'] == request.form['email'] and user['password'] == request.form['password']][0]
                if user != None : session['logged_in'] = True
                return redirect(url_for('home'), code=307)
            except Exception : 
                flash("Invalids credentials",'error')
                return redirect(url_for('login'))
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
    """Register user"""
    if "user_id" in session:
        return redirect(url_for("login"))
    if request.method == "GET":
        return render_template("register.html")
        # loading input from form
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    print(name)
    # validating input
    if name is None or password is None or email is None:
        return render_template("register.html", error="Please fill all fields"), 400

    # check for email already exists
    if user.is_email_exists(email) is not None:
        return render_template("register.html", error="Email already exists"), 403

    user_data = user.register(name, email, password)
    if user_data is None:
       return render_template("register.html", error="Could not add user"), 403

    session["user_id"] = user_data[0]
    session["user_name"] = user_data[1]
    return redirect(url_for("login"))

    users = {}
    users['name'] = name
    users['email'] = email
    users['password'] = password

    {
        "name":"Simply Lift",
        "email":"j@j.co",
        "password":"azerty"
    },
    {
        "name":"Simply Lift",
        "email":"j@j.co",
        "password":"azerty"
    },
    


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