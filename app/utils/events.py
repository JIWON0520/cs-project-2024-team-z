import sqlite3

# 데이터베이스 설정 및 테이블 생성
def setup_database(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            start_date DATE NOT NULL,
            start_time TIME,
            end_date DATE NOT NULL,
            end_time TIME,
            all_day BOOLEAN NOT NULL DEFAULT TRUE,
            memo TEXT 
        )
    ''')
    conn.commit()
    conn.close()

# 이벤트 추가 함수
def add_event(db, username, title, start_date, start_time, end_date, end_time, all_day, memo):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO events (username, title, start_date, start_time, end_date, end_time, all_day, memo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (username, title, start_date, start_time, end_date, end_time, all_day, memo))
    conn.commit()
    conn.close()

# 캘린더에서 이벤트를 로드하는 함수
def load_events(db, username):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT title, start_date, start_time, end_date, end_time, all_day, memo FROM events WHERE username = ?", (username,))
    events = c.fetchall()
    conn.close()
    return [{
        'title': event[0],
        'start': f"{event[1]}T{event[2]}",
        'end': f"{event[3]}T{event[4]}",
        'allDay': event[5],
        "color": "#b3b3ff" if event[6] is None else "#ffb3ff"
    } for event in events]

def fetch_events_for_date(db, username, date):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    # 날짜 형식은 'YYYY-MM-DD'로 가정
    query = '''
        SELECT id, username, title, start_time, end_time, all_day, memo
        FROM events
        WHERE username=? and start_date = ?
    '''
    c.execute(query, (username, date))
    events = c.fetchall()
    conn.close()
    return events