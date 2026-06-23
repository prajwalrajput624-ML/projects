from flask import Flask, render_template, request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask import make_response
from datetime import datetime
import pandas as pd
import joblib
import os

application  = Flask(__name__)
try:
    model = joblib.load('best_model_logistic.pkl')
except:
    model = None
    print("Model file not found. Please ensure 'best_model_logistic.pkl' is in the correct directory.")
    
application.secret_key = 'super_secret_key'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Parental_Involvement = db.Column(db.String(100), nullable=False)
    Access_to_Resources = db.Column(db.String(100), nullable=False)
    Extracurricular_Activities = db.Column(db.String(100), nullable=False)
    Motivation_Level = db.Column(db.String(100), nullable=False)
    Internet_Access = db.Column(db.String(100), nullable=False)
    Family_Income = db.Column(db.String(100), nullable=False)
    Teacher_Quality = db.Column(db.String(100), nullable=False)
    School_Type = db.Column(db.String(100), nullable=False)
    Peer_Influence = db.Column(db.String(100), nullable=False)
    Learning_Disabilities = db.Column(db.String(100), nullable=False)
    Parental_Education_Level = db.Column(db.String(100), nullable=False)
    Distance_from_Home = db.Column(db.String(100), nullable=False)
    Gender = db.Column(db.String(100), nullable=False) 
    Hours_Studied = db.Column(db.Integer, nullable=False)
    Attendance = db.Column(db.Float, nullable=False)
    Sleep_Hours = db.Column(db.Integer, nullable=False)
    Previous_Scores = db.Column(db.Float, nullable=False)
    Tutoring_Sessions = db.Column(db.Integer, nullable=False)
    Physical_Activity = db.Column(db.Integer, nullable=False)
    Prediction_Result = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

with application.app_context():
    db.create_all()

class User_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with application.app_context():
    db.create_all()

@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        un = request.form.get('Username')
        em = request.form.get('Email-Id')
        pw = request.form.get('Password')
        
        if un and em and pw:
            if User_Details.query.filter_by(email=em).first():
                return "Email already registered!" 
                
            user = User_Details(username=un, email=em, password=pw)
            db.session.add(user)
            db.session.commit()
            return render_template('login.html')
    return render_template('register.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        em = request.form.get('Email-Id')
        pw = request.form.get('Password')
        
        user = User_Details.query.filter_by(email=em, password=pw).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            return "Invalid Credentials" 
    return render_template('login.html')
@application.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')

    return render_template('login.html')


@application.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            data = {
                'Parental_Involvement': request.form.get('Parental_Involvement').strip().lower(),
                'Access_to_Resources': request.form.get('Access_to_Resources').strip().lower(),
                'Extracurricular_Activities': request.form.get('Extracurricular_Activities').strip().lower(),
                'Motivation_Level': request.form.get('Motivation_Level').strip().lower(),
                'Internet_Access': request.form.get('Internet_Access').strip().lower(),
                'Family_Income': request.form.get('Family_Income').strip().lower(),
                'Teacher_Quality': request.form.get('Teacher_Quality').strip().lower(),
                'School_Type': request.form.get('School_Type').strip().lower(),
                'Peer_Influence': request.form.get('Peer_Influence').strip().lower(),
                'Learning_Disabilities': request.form.get('Learning_Disabilities').strip().lower(),
                'Parental_Education_Level': request.form.get('Parental_Education_Level').strip().lower(),
                'Distance_from_Home': request.form.get('Distance_from_Home').strip().lower() ,
                'Gender': request.form.get('Gender').strip().lower(),
                'Hours_Studied': int(request.form.get('Hours_Studied')), 
                'Attendance': float(request.form.get('Attendance')), 
                'Sleep_Hours': int(request.form.get('Sleep_Hours')), 
                'Previous_Scores': float(request.form.get('Previous_Scores')), 
                'Tutoring_Sessions': int(request.form.get('Tutoring_Sessions')), 
                'Physical_Activity': int(request.form.get('Physical_Activity'))
                }
            correct_order = [
                "Parental_Involvement", "Access_to_Resources", "Extracurricular_Activities",
                "Motivation_Level", "Internet_Access", "Family_Income", "Teacher_Quality",
                "School_Type", "Peer_Influence", "Learning_Disabilities",
                "Parental_Education_Level", "Distance_from_Home", "Gender",
                "Hours_Studied", "Attendance", "Sleep_Hours", "Previous_Scores",
                "Tutoring_Sessions", "Physical_Activity"
            ]
            df = pd.DataFrame([data])[correct_order]
            prediction = model.predict(df)
            result = "Pass" if prediction[0] == 1 else "Fail"
            student = Student(
                Parental_Involvement=data['Parental_Involvement'],
                Access_to_Resources=data['Access_to_Resources'],
                Extracurricular_Activities=data['Extracurricular_Activities'],
                Motivation_Level=data['Motivation_Level'],
                Internet_Access=data['Internet_Access'],
                Family_Income=data['Family_Income'], 
                Teacher_Quality=data['Teacher_Quality'],
                School_Type=data['School_Type'],
                Peer_Influence=data['Peer_Influence'],
                Learning_Disabilities=data['Learning_Disabilities'],
                Parental_Education_Level=data['Parental_Education_Level'],
                Distance_from_Home=data['Distance_from_Home'],
                Gender=data['Gender'],
                Hours_Studied=data['Hours_Studied'],
                Attendance=data['Attendance'],
                Sleep_Hours=data['Sleep_Hours'],
                Previous_Scores=data['Previous_Scores'],
                Tutoring_Sessions=data['Tutoring_Sessions'],
                Physical_Activity=data['Physical_Activity'],
                Prediction_Result=result
            )
            db.session.add(student)
            db.session.commit()
            return f'<h1 style="color: #2E86C1;">Prediction Result: {result}</h1><p><a href="/">Again Prediction</a></p>'
        except Exception as e:
            return f'prediction during error: {str(e)}<p><a href="/">Go Back</a></p>'
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)






