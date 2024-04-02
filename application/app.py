import streamlit as st
import pandas as pandas
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize 
import connection


st.set_page_config(page_title="Dashboard",page_icon="🌐",layout="wide")
st.subheader("🔔 descriptive Analytics")
st.markdown("##")



result=view_all_data()
df = pd.DataFrame(result, columns=[
    "Patient ID", "Age", "Sex", "Cholesterol", "Blood Pressure", 
    "Heart Rate", "Diabetes", "Family History", "Smoking", "Obesity",
    "...", "Sedentary Hours Per Day", "Income", "BMI", "Triglycerides",
    "Physical Activity Days Per Week", "Sleep Hours Per Day", "Country",
    "Continent", "Hemisphere", "Heart Attack Risk"
])