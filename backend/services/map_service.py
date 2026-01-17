import requests
import json
import os
from config import Config
import math

BIKESHARE_FEEDS = {
    'capital': {
        'name': 'Capital Bikeshare (DC)',
        'station_info': 'https://gbfs.capitalbikeshare.com/gbfs/en/station_information.json',
        'station_status': 'https://gbfs.capitalbikeshare.com/gbfs/en/station_status.json'
    },
    'citibike': {
        'name':  'Citi Bike (NYC)',
        'station_info': 'https://gbfs.citibikenyc. com/gbfs/en/station_information.json',
        'station_status': 'https://gbfs.citibikenyc.com/gbfs/en/station_status.json'
    },
    'divvy': {
        'name':  'Divvy (Chicago)',
        'station_info': 'https://gbfs.divvybikes.com/gbfs/en/station_information.json',
        'station_status': 'https://gbfs.divvybikes.com/gbfs/en/station_status.json'
    }
}

def fetch_live_stations(city='capital'):
    """Fetch live bike station data"""
    try:
        feed = BIKESHARE_FEEDS. get(city)
        if not feed:
            return load_static_stations()

        info_response = requests.get(feed['station_info'], timeout=10)
        info_data = info_response.json()

        status_response = requests.get(feed['station_status'], timeout=10)
        status_data = status_response.json()

        status_map = {}
        for status in status_data. get('data', {}).get('stations', []):
            status_map[status['station_id']] = status

        stations = []
        for station in info_data.get('data', {}).get('stations', []):
            station_id = station['station_id']
            status = status_map.get(station_id, {})

            stations.append({
                'id':  station_id,
                'name': station. get('name', 'Unknown Station'),
                'address': station.get('address', ''),
                'latitude': float(station.get('lat', 0)),
                'longitude': float(station.get('lon', 0)),
                'capacity': station.get('capacity', 0),
                'bikes_available': status.get('num_bikes_available', 0),
                'docks_available': status.get('num_docks_available', 0),
                'ebikes_available': status.get('num_ebikes_available', 0),
                'status': 'active' if status.get('is_renting', 0) == 1 else 'inactive'
            })

        print(f"✓ Fetched {len(stations)} live stations from {feed['name']}")
        return stations

    except Exception as e:
        print(f"Error fetching live stations: {e}")
        return load_static_stations()

def load_static_stations():
    """Load stations from static JSON"""
    try:
        if os.path.exists(Config.STATIONS_DATA_PATH):
            with open(Config. STATIONS_DATA_PATH, 'r') as f:
                stations = json.load(f)
                print(f"✓ Loaded {len(stations)} stations from static file")
                return stations
        return []
    except Exception as e:
        print(f"Error loading static stations:  {e}")
        return []

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance using Haversine formula"""
    R = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math. sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math. atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c * 1000
    return distance

def get_nearby_stations(latitude, longitude, radius=5000, city='capital'):
    """Get nearby stations"""
    stations = fetch_live_stations(city)
    nearby = []

    for station in stations:
        try:
            distance = calculate_distance(latitude, longitude, station['latitude'], station['longitude'])

            if distance <= radius:
                station_copy = station.copy()
                station_copy['distance'] = round(distance, 2)
                station_copy['distance_km'] = round(distance / 1000, 2)
                nearby.append(station_copy)
        except:
            continue

    nearby.sort(key=lambda x: x['distance'])
    return nearby

def get_all_stations(city='capital'):
    """Get all stations"""
    return fetch_live_stations(city)

def get_station_details(station_id, city='capital'):
    """Get station details"""
    stations = fetch_live_stations(city)

    for station in stations:
        if str(station. get('id')) == str(station_id):
            return station

    return None