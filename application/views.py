from flask import Blueprint, render_template, request, redirect, url_for, flash
import pymongo as pm
import pandas as pd
import joblib
from prediction import setup_prediction_model,predictHeartRisk
from connection import db, riskPrediction
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
@views.route('/predict', methods=['POST', 'GET'])
def predict():
    result = None
    if request.method == 'POST':  
        # Convert "Yes" to 1 and "No" to 0 for relevant fields
        def convert_to_int(value):
            return 1 if value == "Yes" else 0
        # Convert Male and Female to 1 and 0
        def convert_sex_int(value):
            return 1 if value =="Male" else 0  
        # Create the user_input DataFrame from form data
        user_input = pd.DataFrame([{
                    'Age': int(request.form['age']),
                    'Cholesterol': int(request.form['cholesterol']),
                    'Heart Rate': int(request.form['heart_rate']),
                    'Diabetes': convert_to_int(request.form['diabetes']),  
                    'Family History': convert_to_int(request.form['family_history']),  
                    'Smoking': convert_to_int(request.form['smoking']), 
                    'Obesity': convert_to_int(request.form['obesity']),  
                    'Alcohol Consumption': convert_to_int(request.form['alcohol_consumption']),
                    'Exercise Hours Per Week': float(request.form['exercise_hours']),
                    'Previous Heart Problems': convert_to_int(request.form['previous_heart_problems']),  
                    'Medication Use': convert_to_int(request.form['medication_use']),  
                    'Stress Level': int(request.form['stress_level']),
                    'BMI': int(request.form['bmi']),
                    'Physical Activity Days Per Week': int(request.form['physical_activity_days']),
                    'Sleep Hours Per Day': int(request.form['sleep_hours']),
                    'Systolic_BP': int(request.form['systolic_bp']),
                    'Diastolic_BP': int(request.form['diastolic_bp']),
                    'Sex_Cat': convert_sex_int((request.form['sex'])),  # Handle as categorical
                    }])
        
        # fetching data from database
        dataset = DataFrame(list(db.mydata.find()))
        dataset = dataset.drop(['_id'], axis=1)
        targetCol = 'Heart Attack Risk'  
        y = dataset[targetCol]
        X = dataset.drop(targetCol, axis=1)
        # prediction model
        predictionModel = setup_prediction_model(X,y)
        prediction = predictHeartRisk(user_input, predictionModel)
        # Determine the result based on the prediction 
        if prediction[0] == 1: 
            result = 'High risk of heart attack'
        else: 
            result = 'Low to No risk of heart attack'

    # Render the appropriate template based on whether result is None or has a value
    return render_template('predict.html', result=result if result is not None else '')


#insert records page
@views.route('/insert-record', methods = ['GET', 'POST'])
def insert_page():
    if request.method == 'POST':
        # Convert "Yes" to 1 and "No" to 0 for relevant fields
        def convert_to_int(value):
            return 1 if value == "Yes" else 0
        # Convert Male and Female to 1 and 0
        def convert_sex_int(value):
            return 1 if value =="Male" else 0
        # Get form data
        record = {
            "Age": int(request.form['age']),
            "Cholesterol": int(request.form['cholesterol']),
            "Heart_rate": int(request.form['heart_rate']),
            "Diabetes": convert_to_int(request.form['diabetes']),
            "Family_history": convert_to_int(request.form['family_history']),
            "Smoking": convert_to_int(request.form['smoking']),
            "Obesity": convert_to_int(request.form['obesity']),
            "Alcohol_consumption": convert_to_int(request.form['alcohol_consumption']),
            "Exercise_hours": int(request.form['exercise_hours']),
            "Previous_heart_problems": convert_to_int(request.form['previous_heart_problems']),
            "Medication_use": convert_to_int(request.form['medication_use']),
            "Stress_level": convert_to_int(request.form['stress_level']),
            "Bmi": int(request.form['bmi']),
            "Physical_activity_days": int(request.form['physical_activity_days']),
            "Sleep_hours": int(request.form['sleep_hours']),
            "Systolic_bp": int(request.form['systolic_bp']),
            "Diastolic_bp": int(request.form['diastolic_bp']),
            "Sex_cat": convert_sex_int((request.form['sex'])),
        }

        # Insert record into MongoDB heartAttackPrediction collection
        db.heartAttackPrediction.insert_one(record)

        return redirect(url_for('views.home_page'))
    else:
        return render_template('insert-record.html')

 
@views.route('/search', methods=['GET', 'POST'])
def search():
       if request.method == 'POST':
        try:
            # Assuming that age inputs are given as integers and sex as 'Male' or 'Female'
            age_min = int(request.form.get('age_min', 0))
            age_max = int(request.form.get('age_max', 100))
            sex = request.form.get('sex')
            diabetes = request.form.get('diabetes')
            obesity = request.form.get('obesity')
            prevHeartDis = request.form.get('prevHD')
            medicationUse = request.form.get('medUse')
            
            # Convert sex into the format stored in your database
            sex_query = 1 if sex == 'Male' else 0
            diabetes_query = 1 if diabetes == 'Diabetes' else 0
            obesity_query = 1 if obesity == 'Obesity' else 0
            prevHeartDis_query = 1 if prevHeartDis == 'Previous heart disease' else 0
            medicationUse_query = 1 if medicationUse == 'Medication use' else 0
            # Construct the query dictionary
            query = {'age': {'$gte': age_min, '$lte': age_max}, 'sex': sex_query, 'diabetes': diabetes_query, 'obesity': obesity_query, 'Previous Heart Problems': prevHeartDis_query, 'Medication Use': medicationUse_query}
         
            results = list(db.heartAttackPrediction.find(query))
            
            # Render the search results template with the query results
            return render_template('search_results.html', results=results)
        
        except ValueError as e:
            # Return an error message if age inputs are invalid
            return f"Invalid input for age: {str(e)}", 400
        
        except Exception as e:
            # Handle any other errors that occur during the search
            return f"An error occurred during the search: {str(e)}", 500

    # Display the search form for GET requests
       return render_template('search.html')

# Define the search_results route if needed for additional processing or a separate results page
@views.route('/search_results', methods=['POST'])
def search_results():
    # This function can be similar to the '/search' POST handler, or used for different form submissions
    pass