from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Sample data
students = [
    {
        'id': 1,
        'name': 'John Doe',
        'age': 20,
        'major': 'Computer Science'
    },
    {
        'id': 2,
        'name': 'Jane Smith',
        'age': 22,
        'major': 'Electrical Engineering'
    }
]

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        major = request.form['major']
        
        # Generate a unique ID for the new student
        new_id = max([student['id'] for student in students]) + 1
        
        new_student = {
            'id': new_id,
            'name': name,
            'age': age,
            'major': major
        }
        
        students.append(new_student)
        
        return redirect('/')
    
    return render_template('add.html')

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    # Find the student with the given ID and remove it from the list
    for student in students:
        if student['id'] == student_id:
            students.remove(student)
            break
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)