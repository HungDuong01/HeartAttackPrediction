from flask import Blueprint, render_template, request, redirect, url_for
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
            # Logic for verifying login credentials
        username = request.form.get('user')
        password = request.form.get('pass')
        user = db.users.find_one({"username": username})  # 'users' is the collection name
        
        if user and user['password'] == password:
            return redirect(url_for('home_page'))  # Redirect to the main page after login
        else:
            return redirect(url_for('login'))
     return render_template('login.html')
#signup page
@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('user-signup')
        password = request.form.get('pass-signup')
        email = request.form.get('email-signup')
        # Insert the new user into the database
        db.users.insert_one({"username": username, "password": password, "email": email})
        return redirect(url_for('login'))
    return redirect(url_for('login'))
#home page
@views.route('/home')
def home_page():
   
    return render_template('index.html')