# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os
import csv

# PAGE CONFIGURATION
csv_path = 'data.csv'
st.set_page_config(page_title="Survey")
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data.csv')
csv_path = os.path.abspath(csv_path)

#Resetting data in csv 
if st.button("Reset CSV Data"):
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Villain", "Times Defeated"])
    st.success("CSV data cleared!")
if os.path.exists(csv_path):
    import pandas as pd
    df = pd.read_csv(csv_path)
    st.dataframe(df)

# --- Ensure CSV file exists with headers ---
if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Villain", "Times Defeated"])

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
# Create text input widgets for the user to enter data.
# The first argument is the label that appears above the input box.
# The submit button for the form.
# This block of code runs ONLY when the submit button is clicked.
    
# --- YOUR LOGIC GOES HERE ---
# TO DO:
# 1. Create a new row of data from 'category_input' and 'value_input'.
# 2. Append this new row to the 'data.csv' file.
#    - You can use pandas or Python's built-in 'csv' module.
#    - Make sure to open the file in 'append' mode ('a')
#    - Don't forget to add a newline character '\n' at the end.
with st.form("survey_form"):
    category_input = st.text_input("Enter a villain:")
    value_input = st.text_input("Enter the amount of times Finn defeated that villain:")

    submitted = st.form_submit_button("Submit Data")

    if submitted:
        if category_input.strip() == "" or value_input.strip() == "":
            st.error("Both fields must be filled out.")
        else:
            new_row = [category_input, value_input]
            try:
                with open(csv_path, "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(new_row)
                st.success(f"Data saved: {category_input} - {value_input}")
            except Exception as e:
                st.error(f"Error writing to CSV: {e}")
# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider()  # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    try:
        df = pd.read_csv(csv_path)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
