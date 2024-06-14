import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from utils.reserv import fetch_hospital_data, calculate_map_bounds
from utils.auth import *
from utils.events import *
from utils.settings import apply_custom_css

def main():
    st.set_page_config(page_title="Reservation", layout='wide', page_icon=":hospital:")
    apply_custom_css()
    login()
    db = 'database/events.db'
    setup_database(db)
    USER = st.session_state['user']
    username = USER[0]
    st.title(":hospital: 병원 예약")

    user_location = [35.2278, 126.8409]  # User's current location(test case)
    hospitals = fetch_hospital_data()
    center_location, bounds = calculate_map_bounds(hospitals, user_location) # Calculate the bounds and center of the map

    map = folium.Map(location=center_location, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(map)

    for hospital in hospitals:
        folium.Marker(
            location=[hospital["lat"], hospital["lon"]],
            popup=f"{hospital['name']}",
            tooltip=hospital["name"]
        ).add_to(marker_cluster)

    folium.Marker(
        location=user_location,
        popup="Your Current Location",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(map)


    map.fit_bounds([[bounds[0], bounds[2]], [bounds[1], bounds[3]]]) # Automatically adjust map to show all markers

    # Display the map in Streamlit
    st_folium(map, width=850, height=500)

    div1, div2 = st.columns(2)
    if 'reservations' not in st.session_state:
        st.session_state['reservations'] = []
        
    with div1:
        # Display a table with a booking button for each hospital
        for hospital in hospitals:
            col1, col2, col3, col4 = st.columns([3, 2, 1, 2])
            with col1:
                st.text(hospital["name"])
            with col2:
                num = hospital["phone"][0:3]+'-'+hospital["phone"][3:6]+'-'+hospital["phone"][6:11]
                st.text(num)
            with col3:
                st.text(hospital["review"] if hospital["review"] is not None else "N/A")
            with col4:
                if st.button("Book Now", key=hospital["name"]):
                    st.session_state['selected_hospital'] = hospital

    with div2:
        if 'selected_hospital' in st.session_state:
            st.subheader(f"Booking for {st.session_state['selected_hospital']['name']}")
            date = st.date_input("Choose a date", key="date")
            time = st.time_input("Choose a time", key="time")
            if st.button("Confirm Booking"):
                add_event(db, username, title=f"{st.session_state['selected_hospital']['name']}", start_date=date, start_time=time.strftime("%H:%M:%S"), end_date=date, end_time=time.strftime("%H:%M:%S"), all_day=False, memo=None)
                st.success(f"You have booked an appointment at {st.session_state['selected_hospital']['name']} on {date} at {time}")
                # reservation_info = {
                #     'hospital_name': st.session_state['selected_hospital']['name'],
                #     'date': date,
                #     'time': time
                # }
                # st.session_state['reservations'].append(reservation_info)
            
if __name__ == "__main__":
    main()
