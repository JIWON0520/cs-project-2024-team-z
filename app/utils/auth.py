import streamlit as st
import sqlite3

def login():
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.sidebar.warning("로그인을 먼저 해주세요.")
        st.stop()

def create_users_table(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL PRIMARY KEY,
            password TEXT NOT NULL,
            due_date DATE NOT NULL,
            baby_nickname TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(db, username, password, due_date, baby_nickname):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, due_date, baby_nickname) VALUES (?, ?, ?, ?)',
              (username, password, due_date, baby_nickname))
    conn.commit()
    conn.close()

def is_authenticated(db, username, password):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user