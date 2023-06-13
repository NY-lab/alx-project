#imports
import random
from flask import Flask, request, render_template, g, url_for, session
from flask_cors import CORS
import mysql.connector
import logging
import bcrypt
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import MySQLdb.cursors, re, hashlib
import secrets

app = Flask(__name__)

# Generate a secure secret key
secret_key = secrets.token_hex(8)

# Use the generated secret key in your Flask application
app.secret_key = secret_key

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="g0thb01",
    database="personality_test"
)

# Create a cursor to execute SQL queries
cursor = db.cursor()

# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get["username"]
        password = request.form.get["password"]
        email = request.form["email"]

         # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

         # Insert user account into the database
        try:
            cursor = db.cursor()
            insert_query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            values = (username, password, email)
            cursor.execute(insert_query, values)
            db.commit()

            #logging.info('Registration successful for user: %s', username)
            return "Registration successful!"
        
        except mysql.connector.Error as err:
            #error_logger.error('Error occurred during registration: %s', err)
            return "Error occurred during registration."

    else:
        return render_template("register.html")
    
if __name__ == "__main__":
    app.run("localhost", 6969, debug=True)
