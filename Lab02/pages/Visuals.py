# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.

import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
csv_data = pd.DataFrame()
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    try:
        csv_data = pd.read_csv("data.csv")
    except:
        st.error("There was an error loading data: 'data.csv'.")
else:
    st.warning("The file 'data.csv' does not exist.")

# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.
if not os.path.exists("data.json"):
    st.warning("The file 'data.json' does not exist.")
elif os.path.getsize("data.json") == 0:
    st.warning("The file 'data.json' is empty.")
else:
    try:
        with open("data.json") as f:
            json_data = json.load(f)
    except json.JSONDecodeError:
        st.error("There was an error loading data: 'data.json' is not valid JSON.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

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
st.subheader("Finn's Recent Battles: Who got Kicked in the Butt?")
if not csv_data.empty:
    csv_data['Value_num'] = pd.to_numeric(csv_data['Value'], errors='coerce')
    data_for_chart = csv_data.groupby('Category')['Value_num'].sum()
    st.bar_chart(csv_data)
    st.write("This represents how many times Finn had to scramble each monster in the week.")
else:
    st.info("No data available.")


# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Battle Stats by Value") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.
# GRAPH 2: DYNAMIC GRAPH
st.subheader("Pick a Power Level: Battle Stats by Value")

st.write(
    "Use the slider to filter Finn’s Fights by minimum value! "
    "The higher you go, the tougher the Villain."
)

if not csv_data.empty:
    csv_data['Value_num'] = pd.to_numeric(csv_data['Value'], errors='coerce')
    csv_data = csv_data.dropna(subset=['Value_num'])
    if not csv_data.empty:
        min_value = int(csv_data['Value_num'].min())
        max_value = int(csv_data['Value_num'].max())
        #NEW store slider value in session state
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
        if not filtered_df.empty:
            grouped = filtered_df.groupby('Category')['Value_num'].sum()
            st.bar_chart(grouped)
            st.write(f"Showing all monster categories where Finn's stat was **≥ {selected_min}**.")



# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Breakdown Of Finn's Monster Vanquishment Three Weeks Ago. ") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.

st.write(
    "Slide to pick the minimum number of times a monster got clobbered by Finn. "
    "Only monsters beaten at least this many times will show up in the chart. "
)
json_file = "data.json"

if not os.path.exists(json_file):
    st.info("No JSON data file found yet.")
else:
    try:
        with open(json_file, "r") as f:
            json_data = json.load(f)
    except json.JSONDecodeError:
        st.error("Uh oh! Couldn't read JSON data. Check your JSON file format.")
    else:
        df_json = pd.DataFrame(json_data.get("data_points", []))

        if df_json.empty:
            st.info("No data points found in JSON.")
        else:
            df_json['value_num'] = pd.to_numeric(df_json['value'], errors='coerce')
            df_json = df_json.dropna(subset=['value_num'])

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

       



        
               
