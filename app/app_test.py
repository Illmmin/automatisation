import pytest
from werkzeug.wrappers import response
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft  import EdgeChromiumDriverManager
import time
from flask import template_rendered

from app import app

#Test des identifiants de connexion
@pytest.mark.parametrize('email ,password, message',[
    ('john@simplylift.co','13',b'Welcome,'), #Test bon
    ('admin@mple.com','op',b'Invalids credentials'), #Test avec un mauvais mail et mauvais mot de passe
    ('admin@mple.com','13',b'Invalids credentials'), #Test avec mauvais mail
    ('john@simplylift.co','op',b'Login User'),#Test avec mauvais mot de passe
    ('john@simplylift.co','',b'Login User'),#Test avec mot de passe vide
    ('','zeezr',b'Login User'), #Test avec email vide
    ('','',b'Login User')]) #Test avec mot de passe et email vide
def test_login_email(email,password, message):
    tester = app.test_client()
    response = tester.post('/login/', data=dict(email=email,password=password), follow_redirects=True)
    assert message in response.data

#Test d'accès sur la page home sans passer par login
def test_redirection_vers_login_home_sans_login():
    tester = app.test_client()
    response = tester.get('/home')
    assert response.status_code == 200 
    assert b'<form' in response.data
    assert b'<input' in response.data
    assert b'<input type="submit" class="btn btn-primary" value="Login" />'  in response.data
    
#Test d'accès sur la page home en passant par login
def test_redirection_vers_login_home_avec_login():
    tester = app.test_client()
    response = tester.post('/login/', data=dict(email="john@simplylift.co",password="13"), follow_redirects=True)
    assert response.status_code == 200
    assert b'<h2>Welcome' in response.data

#Test vérifier que le formulaire de connexion n'accepte pas la méthode GET
def test_login_avec_get():
    tester = app.test_client()
    response = tester.get('/login/', data=dict(email="john@simplylift.co",password="13"), follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

#Fixture qui connecte le user avec les bons identifiants
@pytest.fixture
def connexion():
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.post('/login/', data=dict(email="john@simplylift.co",password="13"), follow_redirects=True)
    assert response.status_code == 200
    yield client

#Test de la fonction logout
def test_log_out(connexion):
    tester = app.test_client()
    response = tester.get('/logout',follow_redirects=True)
    assert response.status_code == 200
    assert b'YOU HAVE SUCCESSFULLY LOGGED OFF!' in response.data

#test mail déja enregistré

#test nouveau utilisateur

#Test de performance

#Test de la page d'erreur : l'utilisateur arrive sur une page d'erreur
@pytest.mark.parametrize('page',[('/'),('/13'),('/Welcome)')])
def test_page_erreur(page):
    tester = app.test_client()
    response = tester.get(page)
    assert response.status_code == 200
    #template = app.jinja_env.get_template('home.html')
    assert b' Hi, this page does not exist,' in response.data

#Test d'accès sur la page home sans passer par login
def test_page_post():
    tester = app.test_client()
    response = tester.get('/post')
    assert response.status_code == 200 
    assert b'<form' in response.data
    assert b'<input' in response.data
    assert b'<input type="submit" class="btn btn-primary" value="Login" />'  in response.data

#Test d'accès sur la page home en passant par login
def test_page_post_2(connexion):
    tester = app.test_client()
    response = connexion.get('/post',follow_redirects=True)
    assert response.status_code == 200
    #template = app.jinja_env.get_template('welcome.html')
    assert b'<title>Post</title>' in response.data

#Faire un test avec un webdriver

# @pytest.fixture(params=["chrome", "firefox"], scope='class')
# def init__driver(request):
#     if request.param == "chrome":
#         options = webdriver.ChromeOptions()
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         web_driver = webdriver.Chrome(ChromeDriverManager(log_level=0, cache_valid_range=7, print_first_line=False).install(), options=options)
#     if request.param == "firefox":
#         web_driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager(log_level=0, cache_valid_range=7, print_first_line=False).install())
#     request.cls.driver = web_driver
#     yield
#     web_driver.close()

# @pytest.mark.usefixtures("init__driver")
# def test_google_title(self):
#     self.driver.get("http://www.google.com")
#     assert self.driver.title == "Google"

