from flask import Blueprint, render_template, request, redirect, url_for
import pymongo as pm
#from extensions import crimes, crimes_pred
#from predictions import setup_prediction_model, predict_crime
from pandas import DataFrame
from datetime import datetime
#from graphs import get_plot, scatter_plot

views = Blueprint('views', __name__)
#login page
@views.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       
        return redirect(url_for('views.home_page'))
    return render_template('login.html')
#signup page
@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        return redirect(url_for('views.login'))
    
    return render_template('signup.html')
#home page
@views.route('/home')
def home_page():
   
    return render_template('index.html')