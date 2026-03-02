# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import os

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Zero Trust Security System",
    page_icon="🔐",
    layout="wide"
)

# =====================================================
# LIGHT PROFESSIONAL CSS
# =====================================================
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f4f7fb;
}

/* Clean white cards */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Buttons */
div.stButton > button:first-child {
    background-color: #2563eb;
    color: white;
    height: 3em;
    width: 100%;
    border-radius: 10px;
    font-weight: 600;
    border: none;
}

div.stButton > button:first-child:hover {
    background-color: #1e40af;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    color: #2563eb !important;
    font-weight: bold;
}

/* Header */
.title-text {
    font-size: 38px;
    font-weight: bold;
    text-align: center;
    color: #1e293b;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">🔐 ZERO TRUST SECURITY SYSTEM</div>', unsafe_allow_html=True)
st.write("")

# =====================================================
# DATABASE SETUP
# =====================================================
DB_FILE = "users.csv"

if not os.path.exists(DB_FILE):
    df = pd.DataFrame({
        "username": ["admin"],
        "password": [hashlib.sha256("admin123".encode()).hexdigest()]
    })
    df.to_csv(DB_FILE, index=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    return pd.read_csv(DB_FILE)

def save_user(username, password):
    users = load_users()
    new_user = pd.DataFrame({
        "username": [username],
        "password": [hash_password(password)]
    })
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(DB_FILE, index=False)

def authenticate(username, password):
    users = load_users()
    hashed = hash_password(password)
    return not users[
        (users["username"] == username) &
        (users["password"] == hashed)
    ].empty

# =====================================================
# SESSION STATE
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "Dashboard"

# =====================================================
# LOGIN / REGISTER
# =====================================================
if not st.session_state.logged_in:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    option = st.radio("Select Option", ["Login", "Register"])

    if option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    else:
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            users = load_users()

            if not new_user or not new_pass:
                st.error("Fill all fields")
            elif new_user in users["username"].values:
                st.warning("Username already exists")
            elif new_pass != confirm:
                st.error("Passwords do not match")
            else:
                save_user(new_user, new_pass)
                st.success("Account created successfully! Please login.")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# AFTER LOGIN
# =====================================================
else:

    st.sidebar.markdown("### Navigation")
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")

    st.session_state.page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Admin Panel", "Logout"],
        index=["Dashboard", "Admin Panel", "Logout"].index(st.session_state.page)
    )

    # ---------------- DASHBOARD ----------------
    if st.session_state.page == "Dashboard":

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(f"Welcome, {st.session_state.username}")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.username == "admin":

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Users", len(load_users()))
            col2.metric("Login Attempts", np.random.randint(20, 50))
            col3.metric("Security Alerts", np.random.randint(0, 5))
            col4.metric("Pending Requests", np.random.randint(1, 10))

            st.markdown("### Login Trends")
            dates = pd.date_range(end=pd.Timestamp.today(), periods=10)
            data = pd.DataFrame({
                "Date": dates,
                "Logins": np.random.randint(20, 100, 10)
            })
            st.line_chart(data.set_index("Date"))

            st.markdown("### Recent Activity")
            activity = pd.DataFrame({
                "User": np.random.choice(load_users()["username"], 5),
                "Action": np.random.choice(
                    ["Login", "Failed Login", "Logout", "Password Change"], 5
                ),
                "Time": pd.date_range(end=pd.Timestamp.now(), periods=5)
            })
            st.dataframe(activity, use_container_width=True)

        else:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Your Activity Score", np.random.randint(70, 100))
            st.write("Access Level: Standard User")
            st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- ADMIN PANEL ----------------
    elif st.session_state.page == "Admin Panel":

        if st.session_state.username == "admin":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Admin Control Center")

            users = load_users()
            cols = st.columns(3)
            for i, user in enumerate(users["username"]):
                with cols[i % 3]:
                    st.info(f"User: {user}")

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning("Admin Access Only")

    # ---------------- LOGOUT ----------------
    elif st.session_state.page == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "Dashboard"
        st.success("Logged out successfully")
        st.rerun()
