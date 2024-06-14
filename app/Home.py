import streamlit as st
from utils.auth import *
from datetime import datetime, date
from utils import settings

def show_login_page(db):
    st.title("Login / Register")

    with st.form(key='login_form'):
        username = st.text_input("ID")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label='Login')
        if submit_button:
            user = is_authenticated(db, username, password)
            if user:
                st.session_state['authenticated'] = True
                st.session_state['user'] = user
                st.rerun()
            else:
                st.error("Incorrect username or password")

    register_expander = st.expander("Register")
    with register_expander:
        with st.form(key='register_form'):
            new_username = st.text_input("ID", key='new_username')
            new_password = st.text_input("New Password", type="password", key='new_password')
            due_date = st.date_input("출산예정일", key='due_date')
            baby_nickname = st.text_input("태명", key='baby_nickname')
            register_button = st.form_submit_button(label='Register')
            if register_button:
                add_user(db, new_username, new_password, due_date, baby_nickname)
                st.success("You are registered, now login")

def show_profile_page():
    user = st.session_state['user']
    due_date = datetime.strptime(user[2], '%Y-%m-%d').date()
    today = date.today()
    d_day = (due_date - today).days
    weeks_pregnant = (280 - d_day) // 7

    # Apply custom CSS for centering the content and adding spacing
    st.markdown("""
        <style>
            .center-content {
                text-align: center;
                margin-top: 10px;  # Add spacing above each element
                margin-bottom: 10px;  # Add spacing below each element
            }
            img {
                margin-top: 20px;
                margin-bottom: 20px;
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        .center-content {
            text-align: center;
            margin-top: 10px;  # Add spacing above each element
            margin-bottom: 10px;  # Add spacing below each element
        }
        img {
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header and details, using custom styles for centering and spacing
    st.markdown(f"<h1 class='center-content' style='color: #ffb3ba;'>Welcome {user[0]}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='center-content' style='color: #ffb3ba;'>🥰{user[3]}🥰</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='center-content' style='color: #ffb3ba;'>태어나기까지 D-{d_day}</h2>", unsafe_allow_html=True)

    # Centered image
    st.markdown(f"<div class='center-content'><img src='https://cdn-icons-png.flaticon.com/512/10217/10217368.png' alt='Baby Icon' width='300'></div>", unsafe_allow_html=True)

    # Additional text with spacing
    st.markdown(f"<h2 class='center-content' style='color: #ffb3ba;'>{user[3]} {weeks_pregnant}주차 무럭무럭 자라고 있는 중🎁</h2>", unsafe_allow_html=True)
    if st.button('Logout', key='logout'):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def main():
    st.set_page_config(page_title="Fetal and Maternal Health Care System", layout='wide', page_icon=":heartbeat:")
    settings.apply_custom_css()

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    db = 'database/users.db'
    create_users_table(db)

    if st.session_state['authenticated']:
        show_profile_page()
    else:
        show_login_page(db)

if __name__ == "__main__":
    main()
