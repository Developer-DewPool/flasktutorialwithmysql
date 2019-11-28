from flask import *
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'rootroot'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)

## POST Method 
@app.route('/', methods=['GET', 'POST'])
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
    
    return render_template('login.html')


## GET Method 
@app.route('/user', methods=['GET', 'POST'])
def getindex():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM MyDB.MyUsers")
    return jsonify(data=cur.fetchall())

if __name__ == '__main__':
    app.run()
