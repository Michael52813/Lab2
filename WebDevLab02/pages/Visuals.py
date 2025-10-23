# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.
import csv

# PAGE CONFIGURATION
st.set_page_config(page_title="Visualizations",)

csv_path = os.path.join(os.path.dirname(__file__), '..', 'data.csv')
csv_path = os.path.abspath(csv_path)
#csv reset being funky
def reset_csv():
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'Value'])
reset_csv()

json_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')
json_path = os.path.abspath(json_path)

if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Value"])
if not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
    default_json = {
        "chart_title": "Finn the Human - Monsters Defeated",
        "data_points": []
    }
    with open(json_path, "w") as f:
        json.dump(default_json, f, indent=4)
# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Loading Data...")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
try:
    csv_data = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"There was an error loading 'data.csv': {e}")
    csv_data = pd.DataFrame()


# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.
try:
    with open(json_path, "r") as f:
        json_data = json.load(f)
except Exception as e:
    st.error(f"There was an error loading 'data.json': {e}")
    json_data = {"chart_title": "Finn the Human - Monsters Defeated", "data_points": []}
        
# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Smackdown Totals") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.
st.write("Finn's Recent Battles: Who got Kicked in the Butt?")
if not csv_data.empty:
    csv_data.columns = csv_data.columns.str.strip().str.replace('\ufeff','')
    if 'Category' in csv_data.columns and 'Value' in csv_data.columns:
        csv_data['Value_num'] = pd.to_numeric(csv_data['Value'], errors='coerce')
        data_for_chart = csv_data.groupby('Category')['Value_num'].sum()
        st.bar_chart(data_for_chart)
        st.write("This represents how many times Finn had to scramble each monster in the week.")
    else:
        st.error("CSV is missing required columns 'Category' or 'Value'. Check your CSV headers!")
else:
    st.info("No CSV data available.")

# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Battle Stats by Value") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.
# GRAPH 2: DYNAMIC GRAPH

st.write(
    "Use the slider to filter Finn’s Fights by minimum value! "
    "The higher you go, the tougher the Villain."
)

if not csv_data.empty:
    #Column names being weird
    csv_data.columns = csv_data.columns.str.strip().str.replace('\ufeff','')
    if 'Category' in csv_data.columns and 'Value' in csv_data.columns:
        csv_data['Value_num'] = pd.to_numeric(csv_data['Value'], errors='coerce')
        csv_data = csv_data.dropna(subset=['Value_num'])
        if not csv_data.empty:
            min_value = int(csv_data['Value_num'].min())
            max_value = int(csv_data['Value_num'].max())
            #NEW storing slider number 
            if 'min_filter_value' not in st.session_state:
            st.session_state.min_filter_value = min_value
            #NEW slider to pick minimum value
            if min_value == max_value:
                max_value = min_value + 1
            selected_min = st.slider(
                "Minimum value:",
                min_value=min_value,
                max_value=max_value,
                value=st.session_state.min_filter_value,
                step=1,
                key="value_slider"
            )
            st.session_state.min_filter_value = selected_min
            filtered_df = csv_data[csv_data['Value_num'] >= selected_min]
            if filtered_df.empty:
                st.info("No battles meet this threshold. Maybe try lowering the slider?")
            else:
                group = filtered_df.groupby('Category')['Value_num'].sum()
                st.bar_chart(group)
                st.write(
                    f"Showing total defeats for each monster where Finn's stat is **≥ {selected_min}**."
                )
        else:
            st.info("No valid numeric data found in 'Value' column.")
    else:
        st.error(csv missing columns)
else:
    st.info("No data found to display this chart.")
        

# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Breakdown Of Finn's Monster Vanquishment Three Weeks Ago. ") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a devoscription and use '#NEW' comments.

st.write(
    "Slide to pick the minimum number of times a monster got clobbered by Finn. "
    "Only monsters beaten at least this many times will show up in the chart. "
)
json_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')
json_path = os.path.abspath(json_path)

if not os.path.exists(json_path):
    st.info("No JSON data file found yet.")
else:
    try:
        with open(json_path, "r") as f:
            json_data = json.load(f)
    except json.JSONDecodeError:
        st.error("Uh oh! Couldn't read JSON data. Check your JSON file format.")
    else:
        st.subheader(json_data.get("chart_title", "Graph 3 Title"))
        df_json = pd.DataFrame(json_data.get("data_points", []))

        if df_json.empty:
            st.info("No data points found in JSON.")
        else:
            df_json['value_num'] = pd.to_numeric(df_json['value'], errors='coerce')
            df_json = df_json.dropna(subset=['value_num'])
            st.write("### Raw JSON Data Points")
            st.dataframe(df_json[['label', 'value_num']])

            if df_json.empty:
                st.info("No numeric data found in JSON to display.")
            else:
                min_defeat = int(df_json['value_num'].min())
                max_defeat = int(df_json['value_num'].max())
                if 'min_defeats_filter' not in st.session_state:
                    st.session_state.min_defeats_filter = min_defeat
                selected_min_defeats = st.slider(
                    "Minimum number of defeats:",
                    min_value=min_defeat,
                    max_value=max_defeat,
                    value=st.session_state.min_defeats_filter,
                    step=1,
                    key="json_defeats_slider"
                )
                st.session_state.min_defeats_filter = selected_min_defeats
                filtered_json = df_json[df_json['value_num'] >= selected_min_defeats]

                if filtered_json.empty:
                    st.info("No monsters meet the minimum threshold. Maybe try lowering the slider?")
                else:
                    chart_data = filtered_json.set_index('label')['value_num']
                    st.bar_chart(chart_data)

                    st.write(
                        f"Monsters Finn defeated at least **{selected_min_defeats}** times in the past week."
                    )

       



        
               
