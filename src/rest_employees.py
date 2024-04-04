import sqlite3
from flask import Flask, request, jsonify, render_template #added to top of file
from flask_cors import CORS #added to top of file

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
#CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5505", "https://wordrow.fun"]}})

def connect_to_db():
    conn = sqlite3.connect('employees.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            PRAGMA foreign_keys = ON;
        ''')

        conn.execute('''
            CREATE TABLE departments (
               department_id INTEGER PRIMARY KEY NOT NULL,
               name TEXT NOT NULL
            );
        ''')

        conn.execute('''INSERT into departments (name) values('Finance');''')
        conn.execute('''INSERT into departments (name) values('Marketing');''');
        conn.execute('''INSERT into departments (name) values('Development');''');
        conn.execute('''INSERT into departments (name) values('Human Resources');''');
        conn.execute('''INSERT into departments (name) values('Sales');''');
        conn.execute('''INSERT into departments (name) values('Legal');''');

        conn.execute('''
            CREATE TABLE locations (
               location_id INTEGER PRIMARY KEY NOT NULL,
               name TEXT NOT NULL
            );
        ''')

        conn.execute('''INSERT into locations (name) values('Boston, MA');''');
        conn.execute('''INSERT into locations (name) values('New York, NY');''');
        conn.execute('''INSERT into locations (name) values('Austin, TX');''');
        conn.execute('''INSERT into locations (name) values('San Diego, CA');''');

        conn.execute('''
            CREATE TABLE employees (
                employee_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                location REFERENCES locations(location_id),
                department REFERENCES locations(department_id)
            );
        ''')

        conn.commit()
        print("Employees table created successfully")
    except:
        print("Employees table creation failed")
    finally:
        conn.close()

def get_locations():
    locations = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM locations")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            location = {}
            location["location_id"] = i["location_id"]
            location["name"] = i["name"]
            locations.append(location)

    except:
        locations = []

    return locations

def get_departments():
    departments = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM departments")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            department = {}
            department["department_id"] = i["department_id"]
            department["name"] = i["name"]
            departments.append(department)

    except:
        departments = []

    return departments

def get_employees():
    employees = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            employee = {}
            employee["employee_id"] = i["employee_id"]
            employee["name"] = i["name"]
            employee["email"] = i["email"]
            employee["phone"] = i["phone"]
            employee["location"] = i["location"]
            employee["department"] = i["department"]
            employees.append(employee)

    except:
        employees = []

    return employees

def insert_employee(employee):
    inserted_employee = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO employees (name, email, phone, location, department) VALUES (?, ?, ?, ?, ?)",
          (employee['name'], employee['email'], employee['phone'], employee['location'], employee['department'])
        )
        conn.commit()
        inserted_employee = get_employee_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_employee

def update_employee(employee):
    updated_employee = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE employees SET name = ?, email = ?, phone =  ?, location = ?, department = ? WHERE employee_id =?",  
                     (employee["name"], employee["email"], employee["phone"], 
                     employee["location"], employee["department"], 
                     employee["employee_id"],))
        conn.commit()
        #return the employee
        updated_employee = get_employee_by_id(employee["employee_id"])

    except:
        conn.rollback()
        updated_employee = {}
    finally:
        conn.close()

    return updated_employee

def get_employee_by_id(employee_id):
    employee = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE employee_id = ?", 
                       (employee_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        employee["employee_id"] = row["employee_id"]
        employee["name"] = row["name"]
        employee["email"] = row["email"]
        employee["phone"] = row["phone"]
        employee["location"] = row["location"]
        employee["department"] = row["department"]
    except:
        employee = {}

    return employee

def delete_employee(employee_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from employees WHERE employee_id = ?",     
                      (employee_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete employee"
    finally:
        conn.close()

    return message

@app.route('/', methods=['GET'])
def index():
    return render_template('employees.html')

@app.route('/bare', methods=['GET'])
def bare():
    return render_template('employees-bare.html')

@app.route('/api/locations', methods=['GET'])
def api_locations():
    return jsonify(get_locations())

@app.route('/api/departments', methods=['GET'])
def api_departments():
    return jsonify(get_departments())

@app.route('/api/employees', methods=['GET','PUT', 'POST'])
def api_employees():
    if request.method == 'GET':
        return jsonify(get_employees())
    elif request.method == 'PUT':
        employee = request.get_json()
        return jsonify(update_employee(employee))
    else:
        employee = request.get_json()
        return jsonify(insert_employee(employee))

@app.route('/api/employees/<employee_id>', methods=['GET','DELETE'])
def api_employee(employee_id):
    if request.method == 'GET':
        return jsonify(get_employee_by_id(employee_id))
    else:
        return jsonify(delete_employee(employee_id))

# Create database if it does not exist
create_db_table();

if __name__ == "__main__":
    app.run() #run app

