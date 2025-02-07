import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime

# Function to load data from an Excel sheet
@st.cache_data
def load_data(sheet_name):
    try:
        return pd.read_excel("attData.xlsx", sheet_name=sheet_name, engine='openpyxl')
    except FileNotFoundError:
        st.error("Excel file not found. Please upload the file.")
        return pd.DataFrame()

# Function to process attendance data
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

    # Normalize data for easier manipulation
    attendance_data = []
    for _, row in df.iterrows():
        if pd.isna(row['Day']) or not str(row['Day']).strip().isdigit():
            continue
        day = int(row['Day'])
        for employee in ['Employee A', 'Employee B', 'Employee C', 'Employee D', 'Employee E', 'Employee F']:
            attendance_data.append({
                "Day": day,
                "Employee": employee,
                "Status": row.get(employee, "-")    # Default status to "-"
            })

    return pd.DataFrame(attendance_data)

# Function to save updated data back to Excel
def save_data_to_excel(updated_df, sheet_name):
    try:
        with pd.ExcelWriter("attData.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            updated_df.to_excel(writer, sheet_name=sheet_name, index=False)
        st.success("Changes saved to Excel file successfully!")
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Load data from the subsheet
data_df = load_data("March")

# Process attendance data into a normalized form
if not data_df.empty:
    processed_data = process_attendance_data(data_df)
else:
    processed_data = pd.DataFrame()

# Get today's day (1-31)
today = datetime.now().day

# Filter data for today's day only
if not processed_data.empty:
    filtered_data = processed_data[processed_data["Day"] == today]
else:   
    filtered_data = pd.DataFrame()

# Display the filtered data
st.header(f"Attendance for Day {today}")

if not filtered_data.empty:
    st.write("Modify attendance status below:")

    # Create a list of updated data to store status changes
    updated_data = pd.read_excel("attData.xlsx",sheet_name=2 )


    # Iterate through each row and allow editing the status
    for index, row in filtered_data.iterrows():
        col1, col2, col3 = st.columns([2, 4, 2])
        with col1:
            st.write(row["Employee"])
        with col2:
            # Dropdown to change the status (can be selected per row)
            status = st.selectbox(
                "Status",
                options=["L", "Y", "N"],
                index=["L", "Y", "N"].index(row["Status"]),
                key=f"{row['Employee']}_{row['Day']}"
            )
        with col3:
            st.write(f"Day {row['Day']}")

        # Append updated data
        #updated_data.append({"Day": row["Day"], "Employee": row["Employee"], "Status": status})
        updated_data.loc[today-1,row["Employee"]]= status
        print(updated_data)

    # Checkbox for confirmation
    confirm = st.checkbox("I confirm to save the changes.")

    # Button to save changes
    if st.button("Save Changes"):
        if confirm:
            # Convert updated data back to DataFrame
            updated_df = pd.DataFrame(updated_data)

            # Save updated data to Excel
            save_data_to_excel(updated_df, "March")
        else:
            st.warning("Please confirm before saving changes.")

else:
    st.info(f"No attendance data found for Day {today}.")

