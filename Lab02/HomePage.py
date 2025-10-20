# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Finn's Saving The Day Tracker")

# INTRODUCTORY TEXT
st.write("""
Welcome to **Finn the Human's** official monster tracking dashboard!

This app is part of **CS 1301 - Web Development Lab 2** and is designed to:
- Record Finn's recent battles in a CSV file
- Visualize how many monsters he's defeated
- Load additional stats from a JSON file

###  How to Use the App:
- **Survey Page**: Add a new monster Finn has defeated this week.
- **Visuals Page**: View the stats of Finn's ulitmate buttkickings throughout the week.

Navigate between pages using the **sidebar** on the left.

""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")
