from flask import Flask, request, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)

# Database configuration
DATABASE = 'personality_test'
DB_HOST = 'http://127.0.0.1'
DB_USER = 'students_access'
DB_PASSWORD = 'g0thb01'

# Establish database connection
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DATABASE
)

#session management
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    # Retrieve the user object from the database
    cursor = db.cursor()
    query = "SELECT id FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        return User(result[0])
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists in the database
        cursor = db.cursor()
        query = "SELECT id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            error_message = "Username already exists. Please choose a different username."
            return render_template('register.html', error_message=error_message)

        # If the username is unique, create a new user account with the provided credentials
        hashed_password = generate_password_hash(password)
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, hashed_password))
        db.commit()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user account information from the database
        cursor = db.cursor()
        query = "SELECT id, password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            hashed_password = result[1]
            if check_password_hash(hashed_password, password):
                # If the credentials are valid, log in the user
                user = User(user_id)
                login_user(user)
                return redirect('/personality_test')

        # Invalid credentials
        error_message = "Invalid username or password. Please try again."
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # Log out the user
    logout_user()
    return redirect('/login')

@app.route('/personality_test')
@login_required
def personality_test():
    # Your personality test code goes here
    return render_template('personality_test.html')

if __name__ == '__main__':
    app.run()
