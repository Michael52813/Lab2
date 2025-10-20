# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import json
import os# The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct path to data.json one level up
json_path = os.path.join(current_dir, '..', 'data.json')

# Normalize path (resolve ..)
json_path = os.path.normpath(json_path)

# Now open json_path
with open(json_path, 'r') as f:
    json_data = json.load(f)
    
# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("Enter a villain:")
    value_input = st.text_input("Enter the amount of times Finn defeated that villain:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    
if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a')
        #    - Don't forget to add a newline character '\n' at the end.
    new_row = [category_input, value_input]

    with open("data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row)

# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
