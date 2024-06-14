def fetch_hospital_data():
    # Example data: list of hospitals with latitude and longitude
    return [
        {"name": "성정희산부인과의원", "lat": 35.2203, "lon": 126.8421, "phone":"0629731113", "review":None},
        {"name": "전남산부인과", "lat": 35.2191, "lon": 126.8424, "phone":"0629721100", "review":None},
        {"name": "첨단하나산부인과의원", "lat": 35.2163, "lon": 126.8428, "phone":"0629730008", "review":None},
        {"name": "첨단미즈여성의원", "lat": 35.2145, "lon": 126.8433, "phone":"0629730043", "review":5.0},
        {"name": "임현정산부인과", "lat": 35.2138, "lon": 126.8435, "phone":"0629743000", "review":4.0},
        {"name": "첨단메디케어의원", "lat": 35.2139, "lon": 126.8506, "phone":"0627209700", "review":3.9},
    ]

def calculate_map_bounds(hospitals, user_location):
    all_lats = [hospital['lat'] for hospital in hospitals] + [user_location[0]]
    all_lons = [hospital['lon'] for hospital in hospitals] + [user_location[1]]
    min_lat, max_lat = min(all_lats), max(all_lats)
    min_lon, max_lon = min(all_lons), max(all_lons)
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    return [center_lat, center_lon], [min_lat, max_lat, min_lon, max_lon]