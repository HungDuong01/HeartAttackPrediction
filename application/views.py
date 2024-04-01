from flask import Blueprint, render_template, request
import pymongo as pm
#from extensions import crimes, crimes_pred
#from predictions import setup_prediction_model, predict_crime
from pandas import DataFrame
from datetime import datetime
#from graphs import get_plot, scatter_plot

views = Blueprint(__name__, 'views')

#main page
@views.route('/')
def index():
    return render_template('login.html')

