from flask import Blueprint, render_template, request, redirect, url_for, flash
import pymongo as pm
#from extensions import crimes, crimes_pred
#from predictions import setup_prediction_model, predict_crime
from connection import db
from pandas import DataFrame
from datetime import datetime
#from graphs import get_plot, scatter_plot

views = Blueprint('views', __name__)
#login page
@views.route('/', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.users.find_one({"email": email})
        if user and user['password'] == password:
            return redirect(url_for('home_page'))  # Redirect to the main page after login
        else:
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