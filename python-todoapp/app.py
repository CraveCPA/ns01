import sqlite3
from flask import Flask, request, render_template, flash, get_flashed_messages, url_for, redirect, session
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "demoapp"

# Initialize database
def init_db():
    #Call sqlite3.connect() to create a connection to the database todo.db in the current working directory, creating it if it does not exist.
    conn = sqlite3.connect("todo.db")

    #In order to execute SQL statements and fetch results from SQL queries, we will need to use a database cursor.
    cur = conn.cursor()

    try:
        #the database cursor object can create table by executing SQL statements.
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
            EMAIL TEXT UNIQUE NOT NULL PRIMARY KEY,
            FULL_NAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TASKS TEXT,
            EMAIL TEXT,
            STATUS TEXT,
            FOREIGN KEY (EMAIL) REFERENCES users(EMAIL)
            )
        ''')
    except Exception as e:
        print(f"Error: {e}")
        
    #Python will not autocommit the transaction performed above hence explicitly committing it.    
    conn.commit()

    #Close the connetion to DB after transactiion so that others can use it.
    conn.close()



# Load welcome page
@app.route('/')
def home():
    # render_Template function will load the given html file form the templates directory.
    return render_template('index.html')



# Load User registration page
@app.route('/register')
def load_user_registeration_page():
    return render_template('registerUser.html')



# Load user login page
@app.route('/login')
def load_user_login_page():

    # Check if the login page is reffered from the user registration page or from welcome page. 
    # This is needed so that if a new user logs in post registration then they are redirected correctly.
    # it is observed that without this the previous logged is session comes into effect if last user didn't log off.
    referrer_url = request.referrer

    if referrer_url:
        parsed_url = urlparse(referrer_url)
        referrer_url = parsed_url.path
        print(referrer_url)

    if referrer_url != '/register' and 'email' in session:
        return redirect('/userlogin')
    else:
        return render_template('userlogin.html')


# Action for new user registration.
@app.route('/addUser', methods=['POST'])
def adduser():
    # get details from the registration form.
    email = request.form.get('email')
    fullname = request.form.get('fullname')
    passwd = request.form.get('password')

    # Connect to the Database
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()

    try:
        # Check if the email is already registered.
        res = cur.execute('SELECT * FROM users WHERE EMAIL==?',(email,))
        user = cur.fetchone()
        
        # If the user is not registered already, then add details from the registration form to DB and redirect to login
        if not user:
            cur.execute('INSERT INTO users (EMAIL, FULL_NAME, PASSWORD) VALUES (?,?,?)',(email,fullname,passwd))
            conn.commit()
            flash("User registered successfully, Please login")
            return redirect('/login')
        else:
            flash("User is already registered.")
            return redirect('/register')

    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()


# Action for when user attempts login.
@app.route('/userlogin', methods=['GET','POST'])
def loginuser():
    # Get the referrer to handle if its a new user or returning user.
    referrer_url = request.referrer

    if referrer_url:
        parsed_url = urlparse(referrer_url)
        referrer_url = parsed_url.path

    if referrer_url == '/login':
        session.clear()

    # if returning User then get details form session cookie else retrieve data from login form and set session cookie.
    if 'email' in session:
        user_email = session['email']
        conn = sqlite3.connect("todo.db")
        cur = conn.cursor()
        print(user_email)
        try:
            # Get all the tasks of logged in user along with status.
            cur.execute('SELECT TASKS,STATUS FROM tasks WHERE EMAIL == ?', (user_email,))
            tasks = cur.fetchall()

            # Get the name of logged in user to display on the user home page.
            cur.execute('SELECT FULL_NAME FROM users WHERE EMAIL == ?', (user_email,))
            fullname = cur.fetchone()[0]
        except Exception as e:
            print(f"Task retrieval error: {e}")
        finally:
            conn.close()

        # Load the user home page with the fetched data.
        return render_template('userhome.html', username=fullname, tasks=tasks or [])
    else:
        email = request.form.get('login-email')
        password = request.form.get('login-password')

        conn = sqlite3.connect("todo.db")
        cur = conn.cursor()

        try:
            # Fetch user info
            cur.execute('SELECT PASSWORD, FULL_NAME FROM users WHERE EMAIL = ?', (email,))
            result = cur.fetchone()

            if result is None:
                return "User not found", 404

            user_passwd, fullname = result

            if user_passwd != password:
                return "User login failed", 401
        
            # If the code reaches here that means user is authenticated, hence set the cookie
            session['email'] = email

            # Fetch user tasks 
            try:
                cur.execute('SELECT TASKS,STATUS FROM tasks WHERE EMAIL = ?', (email,))
                tasks = cur.fetchall()
                print(tasks)
            except Exception as e:
                print(f"Task retrieval error: {e}")
                tasks = [] 

            # Load the user home page along with fetched data.
            return render_template('userhome.html', username=fullname, tasks=tasks or [])

        except Exception as e:
            print(f"Login error: {e}")
            return f"Error occurred: {e}", 500

        finally:
            conn.close()



# Add a new task
@app.route("/addtask", methods=["POST"])
def addtask():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
   
    # Get task form the userhome page form
    task = request.form.get("task")

    # Get user email from session cookie
    email = session['email']

    # A new task will always have a pending status.
    status = 'pending'

    #add task to tasks table
    try:
        cur.execute('INSERT INTO tasks(TASKS, EMAIL, STATUS) VALUES (?,?,?)',(task, email, status))
        flash("Task added successfully!! ")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.commit()
        conn.close()

    # Redirect to the user home page to refresh the new data. 
    return redirect('/userlogin')



# Set the task status to completed
@app.route('/completetask', methods=["GET", "POST"])
def completetask():
    # Get the task text from the form
    task = request.form.get("task")
    
    # Get email from session cookie.
    email = session['email']

    # Set the status to completed.
    status = 'completed'

    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    
    try:
        cur.execute('UPDATE tasks SET STATUS = ? WHERE TASKS == ? AND EMAIL == ?',(status, task, email))
        flash("Task marked as completed ")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.commit()
        conn.close()
    
    return redirect('/userlogin')


# Safely deleting the task of the logged in user.
@app.route('/deletetask', methods=["GET","POST"])
def deletetask():
    # Get the task from user home page, it is a hidden input field in the form component that stores the task.
    task = request.form.get("task")
    
    # Get email from session cookie.
    email = session['email']

    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()

    try:
        cur.execute('DELETE FROM tasks WHERE TASKS == ? AND EMAIL == ?',( task, email))
        flash("Task deleted!! ")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.commit()
        conn.close()

    return redirect('/userlogin')


# Log out the user and clear session cookie
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0')

