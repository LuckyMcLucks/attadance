import streamlit as st

from io import BytesIO
from datetime import datetime, timedelta, date
import time
import calendar
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split 
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler 
from sklearn.preprocessing import normalize 
from sklearn.metrics import accuracy_score

def load_data(sheet_name):
    try:
        return pd.read_excel("attData.xlsx", sheet_name=sheet_name, engine='openpyxl')
    except FileNotFoundError:
        st.error("Excel file not found. Please upload the file.")
        return pd.DataFrame()

def process_attendance_data(df):
    # Rename columns based on actual data
    df = df.rename(columns={
        'Day': 'Day',
        'Unnamed: 2': 'Employee A',
        'Unnamed: 3': 'Employee B',
        'Unnamed: 4': 'Employee C',
        'Unnamed: 5': 'Employee D',
        'Unnamed: 6': 'Employee E',
        'Unnamed: 7': 'Employee F'
    })

    attendance_data = {}
    for _, row in df.iterrows():
        if pd.isna(row['Day']) or not str(row['Day']).strip().isdigit():
            continue
        day = int(row['Day'])
        for employee in ['Employee A', 'Employee B', 'Employee C', 'Employee D', 'Employee E', 'Employee F']:
            if employee in row:
                # Clean the status by stripping spaces and converting to uppercase for consistent comparison
                status = str(row[employee]).strip().upper() if pd.notna(row[employee]) else None
                # Store cleaned status
                attendance_data[(day, employee)] = status

    return attendance_data


#_---------------------------------------------------------
df =  pd.read_excel('AI Data.xlsx',engine='openpyxl' )
X = df["Score"] 
y = df['Bonus']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
k = 3
knn = KNeighborsRegressor(n_neighbors=k)
knn.fit(X_train.values.reshape(-1,1), y_train)
y_predict = knn.predict([[10],[11.1],[19.2],[8.1]])
score = knn.score(X_test.values.reshape(-1,1), y_test)
def get_predict(x_input):
    print(knn.predict([[x_input]]))
    return knn.predict([[x_input]])


col1, col2, col3 = st.columns([1, 3, 1])

def generate_attendance_calendar(year, month, attendance_data, employee):
    # Generate calendar for the specified year and month
    month_calendar = calendar.monthcalendar(year, month)

    calendar_html = "<div style='display: flex; justify-content: center;'><table style='border-collapse: collapse; width: auto; border: 1px solid black;'>"
    calendar_html += "<tr>"
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        calendar_html += f"<th style='border: 1px solid black; padding: 10px; text-align: center; width: 50px; height: 50px;'>{day}</th>"
    calendar_html += "</tr>"

    for week in month_calendar:
        calendar_html += "<tr>"
        for day in week:
            if day == 0:
                calendar_html += "<td style='border: 1px solid black; padding: 10px; width: 50px; height: 50px;'></td>"
            else:
                status = attendance_data.get((day, employee), None)
                # Set color based on status
                if status == "Y":
                    color = "green"
                elif status == "N":
                    color = "red"
                elif status == "L":
                    color = "#FFD700"
                elif status is None:  # No color if status is None (empty)
                    color = "gray"  # Gray for None
                else:
                    color = "gray"  # Fallback for unexpected status

                calendar_html += f"<td style='border: 1px solid black; padding: 10px; background-color: {color}; text-align: center; width: 50px; height: 50px;'>{day}</td>"
        calendar_html += "</tr>"
    calendar_html += "</table></div>"

    return calendar_html

# Fungsi untuk memuat data dari subsheet berdasarkan bulan yang dipilih
def load_data_for_month(month):
    sheet_name = {
        1: "January",
        2: "February",
        3: "March"
    }.get(month)

    if sheet_name:
        return load_data(sheet_name=sheet_name)
    else:
        st.error(f"Subsheets untuk bulan {month} tidak ditemukan.")
        return pd.DataFrame()

def bonus(current_bonus):
    html = "<div style='display: flex; justify-content: center;'>"
    html += "</tr>"
    attendance_ = []
    Weather=[]
    weatherI = {"Stormy":0.1,"Rainy":0.2,"Windy":0.5,"Cloudy":0.8,"Sunny":1}
    #new_bonus = Adjust_bonus(current_bonus)
    today = datetime.today()
    month = calendar.monthrange(today.year, today.month)
    days_left = month[1] - today.day
    df  = pd.read_excel("attData.xlsx",sheet_name="January")
    attandance = df.loc[:,"Employee A"]
    weather = df.loc[:,"Weather"]
    for day in attandance:
        if day == 'Y' :
            attendance_.append(1)
        elif day == "N":
            attendance_.append(0)
        elif day == "L":
            attendance_.append(.5)
        else:
            attendance_.append(1)
        
    for w in weather:
        Weather.append(weatherI[w])

    score = np.sum(np.array(Weather)*np.array(attendance_))
    W_score = np.sum(np.array(Weather))



    new_bonus =round(get_predict(score)[0],-3)
    html += f"<p>Bonus: {new_bonus} ({days_left} Days Left)</p>"
    html+= "</div>"
    return html

def Today():
    html = "<div style='display: flex;'>"
    html += "</tr>"
    #new_bonus = Adjust_bonus(current_bonus)
    day = datetime.today().strftime('%Y-%m-%d')

    html += f"<p>Today: {day}</p>"
    html+= "</div>"
    return html
col1,col2,col3 = st.columns(3)

bonus_amt = 0
days = 10
attendance_data = {
    date(2025, 1, 1): True,
    date(2025, 1, 2): False,
    date(2025, 1, 3): True,
    date(2025, 1, 4): True,
    date(2025, 1, 5): False,
}

# Streamlit App


# State untuk navigasi bulan
if "current_month" not in st.session_state:
    st.session_state.current_month = date.today().month
if "current_year" not in st.session_state:
    st.session_state.current_year = date.today().year

# Batasi navigasi bulan hanya untuk 3 bulan pertama
if st.session_state.current_month > 3:
    st.session_state.current_month = 3
if st.session_state.current_month < 1:
    st.session_state.current_month = 1

data_excel = load_data_for_month(st.session_state.current_month)

if not data_excel.empty:
    attendance_data = process_attendance_data(data_excel)

    # Pilih karyawan (selalu menggunakan Employee C)
    employee = 'Employee A'

    # Generate kalender absensi untuk bulan yang dipilih
    calendar_html = generate_attendance_calendar(
        st.session_state.current_year,
        st.session_state.current_month,
        attendance_data,
        employee
    )
   
with col1:
    if st.session_state.current_month > 1 and st.button("←"):
        st.session_state.current_month -= 1
        print(st.session_state.current_month)
with col3:
    if st.session_state.current_month < 3 and st.button("→"):
        st.session_state.current_month += 1
        print(st.session_state.current_month)
with col2:
    st.markdown(f"### {calendar.month_name[st.session_state.current_month]} {st.session_state.current_year}")
    
    with st.container(border=True):   
        st.markdown(bonus(100),unsafe_allow_html=True)
    st.markdown(calendar_html, unsafe_allow_html=True)
    if st.button("Generate QR code"):
        st.switch_page('pages/3_Streamlit.py')

