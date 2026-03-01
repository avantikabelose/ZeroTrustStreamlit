# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np

# --- Page config ---
st.set_page_config(
    page_title="Zero Trust Project",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Users database ---
USERS = {"admin": "1234", "user": "abcd"}

# --- Session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "Dashboard"

# --- CSS Styling ---
st.markdown("""
<style>
body { background-color: #f0f2f6; }
h1, h2, h3 { color: #2c3e50; }
div.stButton > button:first-child {
    background-color: #1abc9c;
    color: white;
    height: 3em;
    width: 100%;
    border-radius: 10px;
    border: none;
    font-size:16px;
    font-weight:bold;
}
div.stButton > button:first-child:hover { background-color: #16a085; color: white; }
.stMetricValue { color: #2c3e50; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- App Title ---
st.title("🔒 Zero Trust Project")

# --- Login Page ---
if not st.session_state.logged_in:
    st.subheader("Please log in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("❌ Invalid username or password")

# --- Dashboard / Admin Panel ---
if st.session_state.logged_in:
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.session_state.page = st.sidebar.radio(
        "Go to", ["Dashboard", "Admin Panel", "Logout"], 
        index=["Dashboard","Admin Panel","Logout"].index(st.session_state.page)
    )

    # --- Dashboard Page ---
    if st.session_state.page == "Dashboard":
        st.subheader(f"Hello, {st.session_state.username}!")
        st.write("Welcome to your dashboard.")

        if st.session_state.username == "admin":
            # Admin sees confidential metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Active Users", 124, "+5%")
            col2.metric("Login Attempts", 37, "-2%")
            col3.metric("Security Alerts", 3, "+1")
            col4.metric("Pending Requests", 8, "+2")

            st.write("### 🔹 Login Trends")
            dates = pd.date_range(end=pd.Timestamp.today(), periods=10)
            data = pd.DataFrame({
                "Date": dates,
                "Logins": np.random.randint(20, 100, size=10)
            })
            st.line_chart(data.set_index("Date"))

            st.write("### 📝 Recent Activity")
            activity_data = pd.DataFrame({
                "User": ["admin", "user", "user", "admin", "user"],
                "Action": ["Login", "Login", "Failed Login", "Password Change", "Logout"],
                "Time": pd.date_range(end=pd.Timestamp.now(), periods=5)
            })
            st.table(activity_data)

        else:
            # Regular users see limited info
            st.info("You have no access to confidential metrics.")
            st.write("Here’s your basic dashboard info:")
            st.metric("Your Activity Score", 85, "+3%")
            st.write("No confidential data available.")

    # --- Admin Panel ---
    elif st.session_state.page == "Admin Panel":
        if st.session_state.username == "admin":
            st.subheader("👑 Admin Panel")
            st.write("Manage users and monitor system activity:")

            # Users cards
            st.write("### Users List")
            cols = st.columns(3)
            for i, user in enumerate(USERS):
                with cols[i % 3]:
                    st.info(f"👤 {user}")

            # Add new user
            new_user = st.text_input("Add new user (username)")
            new_pass = st.text_input("Password for new user", type="password")
            if st.button("Add User"):
                if new_user and new_pass:
                    if new_user in USERS:
                        st.warning("User already exists.")
                    else:
                        USERS[new_user] = new_pass
                        st.success(f"User {new_user} added!")
                else:
                    st.error("Please enter both username and password.")
        else:
            st.warning("❌ Access Denied: Admins only.")

    # --- Logout ---
    elif st.session_state.page == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "Dashboard"
        st.success("You have been logged out!")