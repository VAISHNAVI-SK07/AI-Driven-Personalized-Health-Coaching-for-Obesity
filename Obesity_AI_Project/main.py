import streamlit as st
import pandas as pd
import sqlite3
import random
import time
from datetime import date

# --- 1. DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT, name TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, weight REAL, bmi REAL, score INTEGER)')
    conn.commit()
    conn.close()

init_db()

# Session States
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

# --- 2. MODERN UI CSS ---
st.set_page_config(page_title="HealthyFitty AI", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #0d1117; color: white; }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 20px; border: 1px solid #30363d; text-align: center;
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #42b883, #34747d);
        color: white; border-radius: 50px; font-weight: bold; font-size: 22px; height: 3.5em; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN/SIGNUP ---
def auth_page():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🥗 HealthyFitty AI</h1>", unsafe_allow_html=True)
        choice = st.radio("Portal", ["Login", "Sign Up"], horizontal=True)
        
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")
        if choice == "Sign Up":
            name = st.text_input("Full Name")
            if st.button("Register & Enter"):
                conn = sqlite3.connect('health_data.db')
                conn.execute("INSERT INTO users VALUES (?,?,?)", (email, pw, name))
                conn.commit()
                st.session_state.update({'logged_in':True, 'user_email':email, 'user_name':name, 'greet':True})
                st.rerun()
        else:
            if st.button("Login"):
                conn = sqlite3.connect('health_data.db')
                user = conn.execute("SELECT * FROM users WHERE email=? AND password=?", (email, pw)).fetchone()
                if user:
                    st.session_state.update({'logged_in':True, 'user_email':user[0], 'user_name':user[2], 'greet':True})
                    st.rerun()

# --- 4. MAIN APP ---
def main_app():
    if st.session_state.get('greet'):
        st.toast(f"Welcome to HealthyFitty, {st.session_state.user_name}! Yes you can do it! 💪")
        st.session_state['greet'] = False

    with st.sidebar:
        st.title(f"Hi, {st.session_state.user_name}")
        w = st.number_input("Weight (kg)", value=0.0)
        h = st.number_input("Height (cm)", value=0.0)
        if st.button("🚪 Sign Out"):
            st.toast("Stay strong! You're doing great! ✨")
            time.sleep(1)
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("# 🚀 HealthyFitty Intelligence")
    
    if st.button("🔍 Check Me"):
        if w > 0 and h > 0:
            bmi = round(w / ((h/100)**2), 2)
            # Calculate a Mock AI Health Score
            score = 100 - int(abs(bmi - 22) * 3)
            score = max(min(score, 100), 10) # Keep between 10-100

            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f"<div class='metric-card'><h4>BMI</h4><h1>{bmi}</h1></div>", unsafe_allow_html=True)
            with c2: 
                status = "Obesity" if bmi >= 30 else "Overweight" if bmi >= 25 else "Healthy"
                st.markdown(f"<div class='metric-card'><h4>Status</h4><h1>{status}</h1></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='metric-card'><h4>AI Health Score</h4><h1 style='color:#42b883;'>{score}%</h1></div>", unsafe_allow_html=True)

            st.divider()
            st.subheader("📋 Personalized Plan")
            plan = ["High Protein Salad", "Lentil Soup", "Nuts", "Grilled Veggies"] if bmi >= 25 else ["Oats", "Rice & Chicken", "Greek Yogurt", "Pasta"]
            st.table(pd.DataFrame({"Meal": ["Breakfast", "Lunch", "Snack", "Dinner"], "AI Guide": plan}))
            
            # Save to DB
            conn = sqlite3.connect('health_data.db')
            conn.execute("INSERT INTO progress VALUES (?,?,?,?,?)", (st.session_state.user_email, str(date.today()), w, bmi, score))
            conn.commit()
            conn.close()
        else:
            st.error("Please enter height and weight in the sidebar!")

# RUN
if st.session_state.logged_in: main_app()
else: auth_page()