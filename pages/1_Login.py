import streamlit as st
import pandas as pd
import numpy as np
import datetime

col1,col2,col3 = st.columns(3)

def load_data():
    file_path = "loginCreds.xlsx"
    df = pd.read_excel(file_path)
    return df

def verify_login(username, password, df):
    user_data = df[df['user'] == username]
    if not user_data.empty:
        if user_data['pass'].values[0] == password:
            return True
    return False


username = st.text_input("Enter your ID")
password = st.text_input("Enter your Password", type='password')

if st.button("Login"):
    data = load_data()
    if verify_login(username, password, data):
        st.success("Success!")
        st.session_state.logged_in = True
        st.session_state.username = username
        st.switch_page('pages/2_Calender.py')
    else:
        st.error("User or Pass is incorrect!")