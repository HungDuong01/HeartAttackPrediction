from flask import Blueprint, render_template, request, redirect, url_for
import pymongo as pm
#from extensions import crimes, crimes_pred
#from predictions import setup_prediction_model, predict_crime
from pandas import DataFrame
from datetime import datetime
#from graphs import get_plot, scatter_plot

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       
        return redirect(url_for('views.home_page'))
    return render_template('login.html')

@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Your signup logic here
        # On successful signup, redirect to the login page
        return redirect(url_for('views.login'))
    # Render the signup page for GET requests
    return render_template('signup.html')
@views.route('/home')
def home_page():
    # The function name is changed to 'home_page' to avoid conflict with the 'home' variable
    return render_template('index.html')