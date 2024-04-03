from flask import Blueprint, render_template, request, redirect, url_for, flash
import pymongo as pm
import pandas as pd
import matplotlib 
matplotlib.use('Agg')
from graphs import get_plot, scatter_plot
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

# Search page  
@views.route('/search', methods=['POST'])
def search():
    # Retrieve form data
    age_min = int(request.form.get('age_min', 0))
    age_max = int(request.form.get('age_max', 100))
    sex = request.form.get('sex', 'Any')  # Default to 'Any' if not provided
    diabetes = request.form.get('diabetes', 'Any')
    obesity = request.form.get('obesity', 'Any')
    prevHeartDis = request.form.get('prevHD', 'Any')
    medicationUse = request.form.get('medUse', 'Any')
    
    # Convert sex into the format stored in your database
    sex_query = 1 if sex == 'Male' else 0 if sex == 'Female' else None
    diabetes_query = 1 if diabetes == 'Yes' else 0 if diabetes == 'No' else None
    obesity_query = 1 if obesity == 'Yes' else 0 if obesity == 'No' else None
    prevHeartDis_query = 1 if prevHeartDis == 'Yes' else 0 if prevHeartDis == 'No' else None
    medicationUse_query = 1 if medicationUse == 'Yes' else 0 if medicationUse == 'No' else None

    # Construct query dictionary, excluding unspecified attributes
    query = {'age': {'$gte': age_min, '$lte': age_max}}
    if sex_query is not None:
        query['sex'] = sex_query
    if diabetes_query is not None:
        query['diabetes'] = diabetes_query
    if obesity_query is not None:
        query['obesity'] = obesity_query
    if prevHeartDis_query is not None:
        query['prevHeartDis'] = prevHeartDis_query
    if medicationUse_query is not None:
        query['medicationUse'] = medicationUse_query

    try:
        results = list(db.heartAttackPrediction.find(query))
        return render_template('search.html', results=results)
    except Exception as e:
        return f"An error occurred during the search: {str(e)}", 500

#####

#Visualize page
@views.route('/visualize', methods=['GET', 'POST'])
def visualize():
   # Queries the database to retrieve the required data
   # Queries the database to retrieve documents where 'Age','Sleep Hours Per Day', and Heart Rate is included
    data = db.heartAttackPrediction.find({
        '$and': [
            {'Age': {'$gt': 10}},  # Specify condition for 'Age' greater than 10
            {'Sleep Hours Per Day': {'$gt': 1}},  # Specify condition for 'Sleep Hours Per Day' greater than 4
            {'Heart Rate': {'$gt': 30}}  # Specify condition for 'Heart Rate' greater than 30
        ]
    }, {'_id': 0, 'Age': 1, 'Sleep Hours Per Day': 1, 'Heart Rate': 1})

    # Convert the retrieved data to a pandas DataFrame
    dataset = pd.DataFrame(list(data))
    
    #Chart for Age
    # Define parameters for the plot
    kind = 'bar'
    title = 'Age Distribution'
    xlabel = 'Age'
    ylabel = 'Number of People'
    sort = True
    limit = 20
    angle = 0  # Adjust the angle if needed

    # Generate plot using get_plot function from graphs.py
    age_plot = get_plot(dataset['Age'], kind, title, xlabel, ylabel, sort, limit, angle)

    #Chart for Sleep Hours
    # Define parameters for the sleep hours per day plot
    sleep_kind = 'bar'
    sleep_title = 'Sleep Hours Distribution'
    sleep_xlabel = 'Sleep Hours'
    sleep_ylabel = 'Number of People'
    sleep_sort = True
    sleep_limit = 10  # Adjust as needed
    sleep_angle = 0  # Adjust as needed

    # Generate plot for sleep hours distribution
    sleep_plot = get_plot(dataset['Sleep Hours Per Day'], sleep_kind, sleep_title, sleep_xlabel, sleep_ylabel, sleep_sort, sleep_limit, sleep_angle)

    #Chart for Age
    # Define parameters for the plot
    kind = 'bar'
    title = 'Heart Rate Distribution'
    xlabel = 'Heart Rate'
    ylabel = 'Number of People'
    sort = True
    heart_limit = 8
    angle = 0  # Adjust the angle if needed

    # Generate plot using get_plot function from graphs.py
    heart_plot = get_plot(dataset['Heart Rate'], kind, title, xlabel, ylabel, sort, heart_limit, angle)

    #query for all Stress Level and Sleep Hours Per Day not equal to 0
    data_scat = db.heartAttackPrediction.find({
    '$and': [
        {'Cholesterol': {'$lt': 200}},  # Specify condition for 'Stress Level' not equal to 0
        {'Heart Rate': {'$lt': 100}}  # Specify condition for 'Sleep Hours Per Day' not equal to 0
    ]
}, {'_id': 0, 'Cholesterol': 1, 'Heart Rate': 1})
    
    dataset_scat = pd.DataFrame(list(data_scat))

    #Chart for scatter
    fieldx = 'Cholesterol'
    fieldy = 'Heart Rate'
    title_scat = 'Chloesterol vs Heart Rate'
    xlabel_scat = 'Cholesterol'
    ylabel_scat = 'Heart Rate'

    scat_plot = scatter_plot(dataset_scat, fieldx, fieldy, title_scat, xlabel_scat, ylabel_scat)


    # Pass the base64-encoded image data to the template
    return render_template('visualize.html', age_plot=age_plot, sleep_plot=sleep_plot, heart_plot=heart_plot, scat_plot=scat_plot)
