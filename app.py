from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'abc'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/employee_management'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define the Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)

# Initialize the LoginManager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define routes for registration and login
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('employee_list'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('login'))

# Define a simple employee list route 
@app.route('/employees')
@login_required
def employee_list():
    employees = Employee.query.all()
    return render_template('employee_list.html', employees=employees)

# Define an employee details route
@app.route('/employee/<int:id>', methods=['GET', 'POST'])
@login_required
def employee_details(id):
    employee = Employee.query.get(id)
    if request.method == 'POST':
        employee.first_name = request.form['first_name']
        employee.last_name = request.form['last_name']
        employee.email = request.form['email']
        employee.department = request.form['department']
        db.session.commit()
        flash('Employee details updated successfully.', 'success')
        return redirect(url_for('employee_list'))
    return render_template('employee_details.html', employee=employee)

# Define a route for handling form submissions with AJAX
@app.route('/submit_form', methods=['POST'])
@login_required
def submit_form():
    data = request.get_json()

    # Process the form data here (e.g., validation, saving to the database)

    response_data = {
        'message': 'Form submitted successfully!',
        'success': True
    }

    return jsonify(response_data)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
