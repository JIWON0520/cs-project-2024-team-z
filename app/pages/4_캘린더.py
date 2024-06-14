import streamlit as st
from streamlit_calendar import calendar
from utils.auth import *
from utils.events import *
from utils.settings import apply_custom_css
from datetime import datetime, timedelta


def main():
    st.set_page_config(page_title="Calendar", layout='wide', page_icon=":calendar:")
    apply_custom_css()

    login()
    db = 'database/events.db'
    setup_database(db)
    
    USER = st.session_state['user']
    username = USER[0]
    st.title(":calendar: My Calendar")

    # 캘린더 표시
    events = load_events(db, username)
    calendar_result = calendar(events=events, options={
        "editable": True,
        "selectable": True,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "slotMinTime": "06:00:00",
        "slotMaxTime": "22:00:00",
        "initialView": "dayGridMonth",
        "height": 600, 
        "eventClick": True
    })
    
    # 이벤트 추가 폼 토글
    with st.expander("일정 추가하기"):
        with st.form("event_form"):
            title = st.text_input("Event Title")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date", start_date)
            start_time = st.time_input("Start Time")
            end_time = st.time_input("End Time")
            all_day = st.checkbox("All Day Event", value=False)
            submit_button = st.form_submit_button("Add Event")
        
        if submit_button:
            add_event(db, username, title, start_date, start_time.strftime("%H:%M:%S"), end_date, end_time.strftime("%H:%M:%S"), all_day, memo=None)
            st.success("Event added successfully!")

    with st.expander("일기 작성하기"):
        with st.form("event_form2"):
            title = st.text_input("Event Title")
            date = st.date_input("Start Date")
            text = st.text_input("Memo")
            submit_button = st.form_submit_button("Add Diary")
        
        if submit_button:
            add_event(db, username, title, start_date=date, start_time="00:00:00", end_date=date, end_time="00:00:00", all_day=1, memo=text)
            st.success("Diary added successfully!")

    if 'callback' in calendar_result:
        if calendar_result['callback'] == "dateClick":
            utc_time_str = calendar_result['dateClick']['date']
            utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            korea_time = utc_time + timedelta(hours=9)  # UTC+9 한국 시간대
            # st.text(f"Korea time: {korea_time.date()}")
            st.subheader(f"Detail in {korea_time.date()}")

            events_on_date = fetch_events_for_date(db, username, str(korea_time.date()))
            if events_on_date:
                for event in events_on_date:
                    id, user, title, start_time, end_time, all_day, memo = event
                    if user == username:
                        if memo == None:
                            # st.write(f"Title: {title}, Start: {start_time}, End: {end_time}, All day: {'Yes' if all_day else 'No'}")
                            with st.container():
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col1:
                                    # st.subheader(f"{event[1]}")
                                    st.markdown(f" - <h5 class='big-font'>{title}</h5>", unsafe_allow_html=True)
                                with col2:
                                    # st.write(f"Start: {event[2]}")
                                    st.markdown(f"<h5 class='big-font'>{start_time}</h5>", unsafe_allow_html=True)
                                with col3:
                                    st.write(f"All day: {'Yes' if all_day else 'No'}")
                                st.markdown("---") 
                        else:
                            with st.container():
                                col1, col2 = st.columns([2, 2])
                                with col1:
                                    st.markdown(f" - <h5 class='big-font'>{title}</h5>", unsafe_allow_html=True)
                                with col2:
                                    st.markdown(f"{memo}", unsafe_allow_html=True)
                                st.markdown("---")
            else:
                st.write("No events on this date.")

if __name__ == "__main__":
    main()
