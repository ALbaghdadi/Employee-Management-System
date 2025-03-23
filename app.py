from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # your MySQL username
        password="admin",  # your MySQL password
        database="employee_db"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee_id = request.form['id']  # Get the employee ID from the form
        full_name = request.form['full_name']
        date_of_birth = request.form['date_of_birth']
        department = request.form['department']
        job_title = request.form['job_title']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO employees (id, full_name, date_of_birth, department, job_title, email, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                       (employee_id, full_name, date_of_birth, department, job_title, email, city, country))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))

    return render_template('add_employee.html')

@app.route('/delete_employee/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
