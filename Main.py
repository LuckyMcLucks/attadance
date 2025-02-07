import streamlit as st
import pandas as pd
import numpy as np
import datetime

col1,col2,col3 = st.columns(3)

pg = st.navigation([
    st.Page("pages/1_Login.py"),
    st.Page("pages/2_Calender.py"),
    st.Page("pages/3_Streamlit.py"),
    st.Page("pages/4_Edit.py")
])
pg.run()


        

        