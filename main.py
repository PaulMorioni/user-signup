from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('user_form.html')
    return template.render()


        
@app.route('/validate', methods=['POST'])
def validate_user():
    username = request.form['username']
    password = request.form['password']
    verifypassword = request.form['verifypassword']
    email = request.form['email']

    username_error =''
    password_error = ''
    verifypassword_error = ''
    email_error = ''

    if len(username) > 3 and len(username) < 20:   # Correct case
        username = username
    else:
        username_error = "Username is invalid (must be between 3 and 20 characters)"
        username = ""

    if len(password) > 3 and len(password) < 20 and ' ' not in password: # Correct Case
        password = password
    else:
        password_error = "Invalid password (must be between 3 and 20 characters, no spaces)"
        password = ''
        verifypassword = ''

    if verifypassword == password: # Correct Case
        verifypassword = verifypassword
    else:
        verifypassword_error = "Passwords do not match"
        password = ''
        verifypassword = ''

    if (len(email) > 3 and len(email) < 20) or email == '': # Correct Case
        if '@' in email and '.' in email and ' ' not in email:
            email = email
        else:
            email_error = "Ivalid Email"
    if email == '':
        email = email
        email_error = ''        

    if username_error== '' and password_error == '' and verifypassword_error == '' and email_error == '':
        return redirect('/valid?username={0}'.format(username))
    else:
        template = jinja_env.get_template('user_form.html')
        return template.render(username=username, password=password, verifypassword=verifypassword, email=email,username_error=username_error, password_error=password_error, verifypassword_error=verifypassword_error, email_error = email_error)

@app.route('/valid')
def valid_user():
    username = request.args.get('username')
    template = jinja_env.get_template('user_greeting.html')
    return template.render(username = username)


app.run()