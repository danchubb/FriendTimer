import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os


# streamlit_app.py

import hmac


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here

# File to store timers
TIMERS_FILE = "timers.json"

# Load timers from file
def load_timers():
    if os.path.exists(TIMERS_FILE):
        with open(TIMERS_FILE, "r") as f:
            return json.load(f)
    return []

# Save timers to file
def save_timers():
    with open(TIMERS_FILE, "w") as f:
        json.dump(st.session_state.timers, f)

# Initialize session state
if 'timers' not in st.session_state:
    st.session_state.timers = load_timers()

# Function to add a new timer
def add_timer(name, target_days):
    st.session_state.timers.append({
        'name': name,
        'date': datetime.now().isoformat(),
        'target_days': target_days
    })
    save_timers()

# Function to delete a timer
def delete_timer(index):
    del st.session_state.timers[index]
    save_timers()

# Function to reset a timer
def reset_timer(index):
    st.session_state.timers[index]['date'] = datetime.now().isoformat()
    save_timers()

# Streamlit UI
st.title("Timer Dashboard")

# Input for new timer
new_timer_name = st.text_input("Timer Name")
new_timer_target = st.number_input("Target Days", min_value=1, step=1)
if st.button("Add Timer"):
    add_timer(new_timer_name, new_timer_target)

# Sorting options
sort_option = st.selectbox("Sort Timers By", ["None", "Alphabetically", "Days Passed"])

# Sort timers based on the selected option
if sort_option == "Alphabetically":
    st.session_state.timers.sort(key=lambda x: x['name'])
elif sort_option == "Days Passed":
    st.session_state.timers.sort(key=lambda x: (datetime.now() - datetime.fromisoformat(x['date'])).days)

# Display timers
for i, timer in enumerate(st.session_state.timers):
    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
    with col1:
        st.write(timer['name'])
    with col2:
        days_passed = (datetime.now() - datetime.fromisoformat(timer['date'])).days
        if days_passed >= timer['target_days']:
            st.markdown(f"<span style='color:red'>{days_passed} days</span>", unsafe_allow_html=True)
        else:
            st.write(f"{days_passed} days")
    with col3:
        st.write(f"Target: {timer['target_days']} days")
    with col4:
        if st.button("Reset", key=f"reset_{i}"):
            reset_timer(i)
    with col5:
        if st.button("Delete", key=f"delete_{i}"):
            delete_timer(i)