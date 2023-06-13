#insert results into database
    db = get_db()
    cursor = db.cursor()

    for question, answers, scores in zip(questions, answer, score):
        cursor.execute("INSERT INTO personalityTestResults (question, answer, score) VALUES (%s, %s, %s)",
                       (question, answer, score))

    db.commit()


run_personality_test()

# MySQL database connection and createTable script
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="g0thb01",
    database="students_db"
)

#function to save the above result to a database

DATABASE = 'personality_test'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(
            host='localhost',
            user='students_access',
            password='g0thb01',
            database=DATABASE
        )
    return db

#create personalityTestResults Table

def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personalityTestResults (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            score INT
        )
    """)
    db.commit()


#Initialize the database and create the table:
with app.app_context():
    create_table()


#Register a function to close the database connection after the request is complete:
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()