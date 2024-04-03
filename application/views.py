from flask import Blueprint, render_template, request, redirect, url_for, flash
import pymongo as pm
import pandas as pd
import joblib
from prediction import setup_prediction_model,predict_heartRisk
from connection import db
from pandas import DataFrame
from datetime import datetime
#from graphs import get_plot, scatter_plot

views = Blueprint('views', __name__)
#login page
@views.route('/', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.users.find_one({"username": username})
        if user and user['password'] == password:
            return redirect(url_for('views.home_page'))  # Redirect to the main page after login
        else:
            flash("Invalid credential")
            return redirect(url_for('views.login'))
     return render_template('login.html')
#signup page
@views.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirmPassword']
            
            if password == confirm_password:
            # Insert the new user into the database
               db.users.insert_one({"username": username, "email": email, "password": password})
               return redirect(url_for('views.login'))
            else:  
                flash("Password doesn't match")
                return redirect(url_for('views.signup'))
     return render_template('signup.html')
#home page
@views.route('/home')
def home_page():
    
    return render_template('Index.html')

@views.route('/visualize')
def visualize():
    
    return render_template('visualize.html')


#preidction page
@views.route('/predict', methods=['POST','GET'])
def predict():
    premise_dict = {
        0: 'Age',
        1: 'Cholesterol',
        2: 'Heart Rate',
        3: 'Family History',
        4: 'Smoking',
        5: 'Obesity',
        6: 'Alcohol Consumption',
        7: 'Exercise Hours per Week',
        8: 'Previous Heart Problems',
        9: 'Medication Use',
        10: 'Stress Level',
        11: 'BMI',
        12: 'Physical Activity Days per Week',
        13: 'Sleep Hours per Day',
        14: 'Systolic_BP',
        15: 'Diastolic_BP',
        16: 'Sex_Cat'
    }
    if request.method == 'POST':
        # get premise from form
        premise = int(request.form['premise'])
        
        # get date from form
        age = request.form['Age']
        chol = request.form['Cholesterol']
        heartRate = request.form['Heart Rate']
        diabetes = request.form['Diabetes']
        famHistory = request.form['Family Hisory']
        smoking = request.form['Smoking']
        obesity = request.form['Obesity']
        alcoholCon = request.form['Alcohol Consumption']
        execisePerWeek = request.form['Exercise Hours Per Week']
        prevHeartProb = request.form['Previous Heart Problems']
        medication = request.form['Medication Use']
        stressLev = request.form['Stress Level']
        bmi = request.form['BMI']
        physActDays = request.form['Physical Activity Days Per Week']
        sleepHrs = request.form['Sleep Hours Per Day']
        sys_BP = request.form['Systolic_BP']
        dia_BP = request.form['Diastolic_BP']
        sexCate = request.form['Sex_Cat']
        
        # create data frame    
        user_input = DataFrame({'Age':[age],
                           'Cholesterol': [chol],
                           'Heart Rate': [heartRate],
                           'Diabetes': [diabetes],
                           'Family History': [famHistory],
                           'Smoking': [smoking],
                           'Obesity':[obesity],
                           'Alcohol Consumption':[alcoholCon],
                           'Exercise Hours Per Week':[execisePerWeek],
                           'Previous Heart Problems':[prevHeartProb],
                           'Medication Use':[medication],
                           'Stress Level':[stressLev],
                           'BMI':[bmi],
                           'Physical Activity Days Per Week':[physActDays],
                           'Sleep Hours Per Day':[sleepHrs],
                           'Systolic_BP':[sys_BP],
                           'Diastolic_BP':[dia_BP],
                           'Sex_Cat':[sexCate]
                           })
           # Create DataFrame from user input
        user_df = pd.DataFrame([user_input])

    
    return render_template('predict.html')

#insert records page
@views.route('/insert-record', methods = ['GET', 'POST'])
def insert_page():
    if request.method == 'POST':
        # Get form data
        record = {
            "age": request.form['age'],
            "sex": request.form['sex'],
            "cholesterol": request.form['cholesterol'],
            "heart_rate": request.form['heart_rate'],
            "diabetes": request.form['diabetes'],
            "family_history": request.form['family_history'],
            "smoking": request.form['smoking'],
            "obesity": request.form['obesity'],
            "alcohol_consumption": request.form['alcohol_consumption'],
            "exercise_hours": request.form['exercise_hours'],
            "previous_heart_problems": request.form['previous_heart_problems'],
            "medication_use": request.form['medication_use'],
            "stress_level": request.form['stress_level'],
            "bmi": request.form['bmi'],
            "physical_activity_days": request.form['physical_activity_days'],
            "sleep_hours": request.form['sleep_hours'],
            "systolic_bp": request.form['systolic_bp'],
            "diastolic_bp": request.form['diastolic_bp']
        }

        # Insert record into MongoDB heartAttackPrediction collection
        db.heartAttackPrediction.insert_one(record)

        return redirect(url_for('views.home_page'))
    else:
        return render_template('insert-record.html')
    
@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Extract and convert the age range and sex from the form data
        # For simplicity, we're assuming age is directly usable as an integer
        try:
            age_min = int(request.form.get('age_min', 0))
            age_max = int(request.form.get('age_max', 100))
            sex = request.form['sex']
        except ValueError as e:
            # Handle case where the conversion fails
            return f"Invalid input for age. Error: {str(e)}"

        try:
            # Aggregation pipeline to match criteria and join collections
            pipeline = [
                {
                    '$match': {
                        'age': {'$gt': age_min, '$lt': age_max},
                        'sex': sex
                    }
                },
                {
                    '$lookup': {
                        'from': 'patient_details',  # The collection to join
                        'localField': 'PatientID',  # Field in this collection
                        'foreignField': 'PatientID',  # Field in the collection to join
                        'as': 'details'  # Alias for the output array
                    }
                },
                {
                    '$unwind': '$details'  # Deconstructs the array
                },
                {
                    '$project': {
                        'age': 1,
                        'sex': 1,
                        'PatientID': 1,
                        'Details': '$details'
                    }
                }
            ]
            results = list(collection.aggregate(pipeline))

            # Render the template with the search results
            return render_template('search_results.html', results=results)
        except Exception as e:
            # Handle errors during the search process
            return f"An error occurred during the search: {str(e)}"
    
    # Display the search form for GET requests
    return render_template('search.html')

# Define the search_results route if needed for additional processing or a separate results page
@views.route('/search_results', methods=['POST'])
def search_results():
    # This function can be similar to the '/search' POST handler, or used for different form submissions
    pass