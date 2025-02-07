import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime

def update_excel(status):
    file_path = 'attData.xlsx'

    today = datetime.today()
    day_today = today.day
    month_today = today.strftime('%B')

    if not os.path.exists(file_path):
        st.error(f"File Excel '{file_path}' tidak ditemukan.")
        return

    try:
        df = pd.read_excel(file_path, sheet_name=month_today, engine='openpyxl')

        if day_today in df['Day'].values:
            df.loc[df['Day'] == day_today, 'Employee A'] = status
        else:
            new_row = {
                'Day': day_today, 
                'Employee A': status, 
                'Employee B': 'N', 
                'Employee C': 'N', 
                'Employee D': 'N', 
                'Employee E': 'N', 
                'Employee F': 'N'
            }
            df = df.append(new_row, ignore_index=True)

        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=month_today, index=False)

        st.success(status)
    except Exception as e:
        st.error(f"Error : {e}")

st.write("Today's QR Code")
st.image("https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg")
st.write()

if st.button('Done'):
    update_excel('Y')
    
    st.switch_page('pages/2_Calender.py')

col1, col2, col3 = st.columns(3)
ph = st.empty()
N = 5*2
for secs in range(N, 0, -1):
    mm, ss = secs // 60, secs % 60
    ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
    time.sleep(1)
ph.metric("Countdown", "DONE")

update_excel('N')
st.switch_page('pages/2_Calender.py')