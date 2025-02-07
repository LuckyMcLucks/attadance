import streamlit as st
from datetime import date, timedelta
import calendar
import pandas as pd

# Fungsi untuk memuat data dari subsheet
@st.cache_data
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
        1: "january",
        2: "february",
        3: "march"
    }.get(month)

    if sheet_name:
        return load_data(sheet_name=sheet_name)
    else:
        st.error(f"Subsheets untuk bulan {month} tidak ditemukan.")
        return pd.DataFrame()

# Streamlit App
st.title("Kalender Absensi Karyawan")

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

# Muat data berdasarkan bulan yang dipilih
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

    st.markdown(f"### {calendar.month_name[st.session_state.current_month]} {st.session_state.current_year}")
    st.markdown(calendar_html, unsafe_allow_html=True)

    # Navigasi bulan menggunakan tombol arah
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.session_state.current_month > 1 and st.button("←"):
            st.session_state.current_month -= 1
    with col3:
        if st.session_state.current_month < 3 and st.button("→"):
            st.session_state.current_month += 1
else:
    st.warning("Tidak ada data yang dapat ditampilkan.")