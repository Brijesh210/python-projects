from flask import Flask
from flask import render_template,  request, session
import sqlite3
import os

app = Flask("Products management")

DATABASE = 'db\\database.db'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def add_user(username, password, admin):
    sql_connection = sqlite3.connect(DATABASE)
    cursor = sql_connection.cursor()
    cursor.execute('INSERT INTO USERS (username, password, admin) VALUES (?,?,?)', (username, password, admin))
    sql_connection.commit()
    sql_connection.close()


def get_all(table: str):
    sql_con = sqlite3.connect(DATABASE)
    cursor = sql_con.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    sql_con.close()
    return rows


def create_tables():
    sql_connection = sqlite3.connect(DATABASE)
    sql_connection.execute('CREATE TABLE USERS ('
                           'username TEXT NOT NULL PRIMARY KEY, '
                           'password TEXT NOT NULL,'
                           'admin BOOL DEFAULT FALSE)')

    sql_connection.execute('CREATE TABLE PRODUCTS ('
                           'ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                           'NAME TEXT,'
                           'QUANTITY INTEGER)')
    sql_connection.close()
    add_user('admin', 'admin', True)
    print("Database created")


def get_user(username: str):
    sql_connection = sqlite3.connect(DATABASE)
    cursor = sql_connection.cursor()
    cursor.execute(f"SELECT * FROM USERS WHERE USERNAME='{username}'")
    user = cursor.fetchall()
    sql_connection.close()
    print(user)
    if len(user) >= 1:
        return user[0]
    return None


@app.route('/')
def index():
    if 'username' not in session:
        return render_template('login.html')
    products = get_all("PRODUCTS")
    return render_template('index.html', products=products)


@app.route('/user/<username>')
def profile(username):
    if session.keys().__contains__('admin'):
        if session['admin']:
            user = get_user(username)
            print(user)
            return render_template('user.html', user=user)
    return "<h2>Admin rights required to visit this page!</h2><br><a href='/'>Main Page</a>"


@app.route('/users')
def users():
    if session.keys().__contains__('admin'):
        if session['admin']:
            all_users = get_all("USERS")
            return render_template('users.html', users=all_users)
    return "<h2>Admin rights required to visit this page!</h2><br><a href='/'>Main Page</a>"


@app.route('/login', methods=['POST'])
def login():
    username: str = request.form['login']
    passwd = request.form['password']
    user = get_user(username.lower())
    if user is not None:
        password = user[1]
        if password is not None and password == passwd:
            session['username'] = username
            session['admin'] = user[2]
            return index()
    return "<h1>Wrong username/password combination! Try again!</h1>" + render_template("login.html")


@app.route('/logout', methods=['GET'])
def logout():
    # If the user session exists - remove it
    if 'username' in session:
        session.pop('username')
        session['admin'] = False
    return "<h2>Logged out</h2> <br>  <a href='/'> Main Page </a>"


@app.route('/add-product', methods=['POST'])
def add_product():
    name = request.form['product_name']
    quantity = request.form['product_quantity']

    sql_con = sqlite3.connect(DATABASE)
    cursor = sql_con.cursor()
    cursor.execute('INSERT INTO PRODUCTS (NAME, QUANTITY) VALUES (?,?)', (name, quantity))
    sql_con.commit()
    return f"<h2> Product {name} added</h2>" + index()


@app.route('/add-user', methods=['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    admin = True if request.form.get('admin') else False
    if len(username) >= 5 and len(password) >= 5:
        if get_user(username):
            return f"<h2>User {username} already exists<h2><br>" + users()
        add_user(username, password, admin)
        return f"<h2>User {username} added<h2><br>" + users()
    else:
        return f"<h2>Username and password must be longer than 5!<h2><br>" + users()


@app.route('/delete', methods=['GET'])
def delete_user():
    user = request.args.get('username')
    if user:
        if user == 'admin' or session['username'] == user:
            return "<h3>Cannot delete currently active admin! Be careful!</h3><br>" + users()
        con = sqlite3.connect(DATABASE)
        try:
            cur = con.cursor()
            cur.execute(f"delete from USERS where USERNAME = '{user}'")
            con.commit()
        except:
            print("Failed to delete " + str(user))
        finally:
            con.close()
            return users()


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        create_tables()

    app.run(debug=True)
