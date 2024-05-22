from flask import Flask, request, render_template, redirect, session, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Serve static files from the 'static' directory
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='student')  # Default role is 'student'

# Define Course model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    print("Inside register route")
    if request.method == 'POST':
        data = request.json
        if data:
            username = data.get('username')
            password_hash = data.get('password')
            role = data.get('role', 'student')  # Default role is student if not provided
            if username and password_hash:
                print("Creating new user:", username)
                new_user = User(username=username, password_hash=password_hash, role=role)
                with app.app_context():
                    db.session.add(new_user)
                    db.session.commit()
                print("User registered successfully")
                return redirect(url_for('login'))
            else:
                return jsonify({'error': 'Missing username or password'}), 400
        else:
            return jsonify({'error': 'No JSON data received'}), 400
    return render_template('register.html')


from flask import jsonify

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        if data:
            username = data.get('username')
            password_hash = data.get('password')  # Hashed password from client
            user = User.query.filter_by(username=username).first()
            if user:
                # Compare the hashed password with the one stored in the database
                if password_hash == user.password_hash:
                    session['user_id'] = user.id
                    session['role'] = user.role  # Set user's role in session
                    # Convert 'User' object to dictionary
                    user_dict = {'id': user.id, 'username': user.username, 'role': user.role}
                    return jsonify({'message': 'Login successful', 'user': user_dict}), 200
                else:
                    return jsonify({'error': 'Invalid username or password'}), 401
            else:
                return jsonify({'error': 'Invalid username or password'}), 401
        else:
            return jsonify({'error': 'No JSON data received'}), 400
    else:
        # Retrieve the user from the session if available
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first() if user_id else None
        return render_template('login.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if 'user_id' not in session:
        return redirect('/login')
    
    # Retrieve user's role from session
    user_id = session.get('user_id')
    print("User ID:", user_id)  # Debug statement
    user = User.query.filter_by(id=user_id).first()
    print("User:", user)  # Debug statement
    user_role = user.role if user else None
    print("User Role:", user_role)  # Debug statement



    
    if request.method == 'POST':
        # Check if user is a teacher before allowing course creation
        if user_role == 'teacher':
            course_name = request.form['name']
            new_course = Course(name=course_name)
            with app.app_context():
                db.session.add(new_course)
                db.session.commit()
            return redirect('/courses')
        else:
            return "You don't have permission to add courses."

    # For GET request, fetch existing courses and render courses.html template
    courses = Course.query.all()
    return render_template('courses.html', courses=courses, user_role=user_role, user=user)



if __name__ == '__main__':
    app.run(debug=True)
