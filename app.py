from flask import *
from flask_mysqldb import MySQL
import MySQLdb
import re


app = Flask(__name__)

app.secret_key = 'ssIsIW234#_!~SD22a5'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'rootroot'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)



## User Login with session
@app.route('/login', methods=['GET', 'POST'])
def login():
        # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM MyDB.accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            # session['id'] = account['id']
            session['username'] = account['username']
            user = session['username']
            # Redirect to home page
            return redirect(url_for('success'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)


## User name display with active session
@app.route('/')
def success():
    try:
        if session['loggedin']:
            return render_template('user.html', name = session['username'])
        else:
            return render_template('user.html')
    except KeyError:
        return render_template('user.html', info= 'Loggin Or registrations First')


## User name display with deactive session
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        passwrd = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM MyDB.accounts WHERE username = %s AND email = %s', (username, email))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cursor.execute("INSERT INTO accounts(username, password, email) VALUES (%s, %s, %s)", (username, passwrd, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))

    return render_template('register.html', msg=msg)


## normal POST Method 
@app.route('/dashboard', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('getindex'))
    
    return render_template('index.html', name = session['username'])

## normal json response GET Method 
@app.route('/user', methods=['GET', 'POST'])
def getindex():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM MyDB.MyUsers")
    return jsonify(data=cur.fetchall())





if __name__ == '__main__':
    app.run()
