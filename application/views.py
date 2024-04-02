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
            flash(username)
            flash(password)
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
@views.route('/prediction', method=['POST','GET'])
def prediction():
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

    
    return render_template('prediction.html')