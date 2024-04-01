from flask import Blueprint, render_template, request, redirect
import pymongo as pm
from connection import records

from datetime import datetime


views = Blueprint(__name__, 'views')

#main page
@views.route('/')
def index():
    return render_template('login.html')

#login page
@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data here and validate
        return redirect('/dashboard')
    return render_template('login.html')
