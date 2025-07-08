from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import json

from models import db
from models.tip import Tip  

# === Flask App Setup ===
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tips.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.secret_key = 'your-secret-key'  

# === Ensure uploads folder exists ===
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# === Initialize DB ===
db.init_app(app)
with app.app_context():
    db.create_all()


# === Routes ===

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit_tip():
    if request.method == 'POST':
        corruption_type = request.form.get('corruption_type')
        location = request.form.get('location')
        date = request.form.get('date')
        people = request.form.get('people')
        tip_category = request.form.get('tip_category')
        description = request.form.get('description')
        uploaded_file = request.files.get('file')
        filename = None

        # Save file if uploaded
        if uploaded_file and uploaded_file.filename:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            uploaded_file.save(file_path)

        # Save to the database
        new_tip = Tip(
            corruption_type=corruption_type,
            location=location,
            date=date,  # string (e.g. "2025-07-08")
            people=people,
            tip_category=tip_category,
            description=description,
            file=filename,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_tip)
        db.session.commit()

        return redirect(url_for('thank_you'))

    return render_template('submit_tip.html')


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '1234':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    tips = Tip.query.order_by(Tip.timestamp.desc()).all()
    return render_template('admin_dashboard.html', tips=tips)


# === Run App ===
if __name__ == '__main__':
    with app.app_context():
        from models import db
        db.create_all()
    app.run(debug=True, port=5001)
