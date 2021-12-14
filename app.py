# pip install flask

from flask import Flask, render_template, request, redirect, url_for

# Instancier la web app 
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def text_box():
    text = request.form['text']
    processed_text = text.upper()
    return render_template("bienvenue.html", message = processed_text)
    
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again'
        else:
            # return redirect(url_for('admin_page'))
            return render_template("admin_page.html")
    return render_template('login.html', error=error)    

if __name__ == '__main__':
    app.run(debug = True)
