import React, { useState, useEffect, useCallback } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import api from '../../services/api';
import { toast } from 'react-toastify';
import 'leaflet/dist/leaflet.css';
import '../../styles/BikeStations.css';

// Fix for default marker icons in React Leaflet
delete L.Icon.Default. prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare. com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare. com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom marker icons based on bike availability
const createCustomIcon = (color) => {
  return new L.Icon({
    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow. png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });
};

const greenIcon = createCustomIcon('green');
const yellowIcon = createCustomIcon('yellow');
const redIcon = createCustomIcon('red');
const blueIcon = createCustomIcon('blue');

// Component to recenter map
function RecenterMap({ center }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, map.getZoom());
  }, [center, map]);
  return null;
}

const BikeStations = () => {
  const [stations, setStations] = useState([]);
  const [userLocation, setUserLocation] = useState(null);
  const [mapCenter, setMapCenter] = useState([38.9072, -77.0369]); // DC default
  const [loading, setLoading] = useState(true);
  const [city, setCity] = useState('capital');

  const fetchNearbyStations = useCallback(async (lat, lng) => {
    try {
      const { data } = await api. post('/stations/nearby', {
        latitude: lat,
        longitude: lng,
        radius: 5000,
        city,
      });
      setStations(data.stations || []);
    } catch (error) {
      console.error('Error fetching nearby stations:', error);
    }
  }, [city]);

  const getUserLocation = useCallback(() => {
    if (navigator. geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location = [position.coords.latitude, position. coords.longitude];
          setUserLocation(location);
          setMapCenter(location);
          fetchNearbyStations(position. coords.latitude, position.coords. longitude);
        },
        (error) => {
          console. log('Location error:', error);
          toast.info('Using default location. Enable location for nearby stations.');
        }
      );
    }
  }, [fetchNearbyStations]);

  const fetchStations = useCallback(async () => {
    try {
      setLoading(true);
      const { data } = await api.get(`/stations/all?city=${city}`);
      setStations(data.stations || []);

      if (data.stations && data. stations. length > 0) {
        setMapCenter([data.stations[0].latitude, data.stations[0].longitude]);
      }
    } catch (error) {
      console.error('Error fetching stations:', error);
      toast.error('Failed to load bike stations');
    } finally {
      setLoading(false);
    }
  }, [city]);

  useEffect(() => {
    fetchStations();
    getUserLocation();
  }, [fetchStations, getUserLocation]);

  const getMarkerIcon = (station) => {
    if (!station. capacity || station.capacity === 0) return yellowIcon;

    const percentage = (station.bikes_available / station.capacity) * 100;
    if (percentage > 50) return greenIcon;
    if (percentage > 20) return yellowIcon;
    return redIcon;
  };

  const getDirections = (station) => {
    const url = `https://www.openstreetmap.org/directions? from=&to=${station.latitude},${station.longitude}`;
    window.open(url, '_blank');
  };

  const centerOnStation = (station) => {
    setMapCenter([station.latitude, station.longitude]);
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading bike stations...</p>
      </div>
    );
  }

  return (
    <div className="bike-stations-container">
      <div className="stations-header">
        <h1>🚴 Bike Stations Map</h1>
        <p>Find nearby bike-sharing stations with OpenStreetMap (Free & Open Source! )</p>
      </div>

      {/* City Selector */}
      <div className="city-selector">
        <label>Select City:</label>
        <select value={city} onChange={(e) => setCity(e.target.value)}>
          <option value="capital">Mumbai</option>
          <option value="citibike">Delhi</option>
          <option value="divvy">Banglore</option>
          <option value="divvy">Kochi</option>

        </select>
      </div>

      {/* Statistics */}
      <div className="stats-cards">
        <div className="stat-card">
          <div className="stat-icon">📍</div>
          <div className="stat-content">
            <h3>Total Stations</h3>
            <p className="stat-number">{stations.length}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🚲</div>
          <div className="stat-content">
            <h3>Available Bikes</h3>
            <p className="stat-number">
              {stations.reduce((sum, s) => sum + (s.bikes_available || 0), 0)}
            </p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🅿️</div>
          <div className="stat-content">
            <h3>Available Docks</h3>
            <p className="stat-number">
              {stations.reduce((sum, s) => sum + (s.docks_available || 0), 0)}
            </p>
          </div>
        </div>
      </div>

      {/* OpenStreetMap */}
      <div className="map-container">
        <MapContainer
          center={mapCenter}
          zoom={13}
          style={{ height: '600px', width: '100%', borderRadius: '15px' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <RecenterMap center={mapCenter} />

          {/* User Location Marker */}
          {userLocation && (
            <Marker position={userLocation} icon={blueIcon}>
              <Popup>
                <div className="popup-content">
                  <h3>📍 Your Location</h3>
                  <p>You are here</p>
                </div>
              </Popup>
            </Marker>
          )}

          {/* Station Markers */}
          {stations.map((station) => (
            <Marker
              key={station.id}
              position={[station.latitude, station.longitude]}
              icon={getMarkerIcon(station)}
            >
              <Popup>
                <div className="popup-content">
                  <h3>{station. name}</h3>
                  <p className="popup-address">{station.address}</p>

                  <div className="popup-stats">
                    <div className="popup-stat">
                      <span className="popup-icon">🚲</span>
                      <span className="popup-label">Bikes:  </span>
                      <span className="popup-value">{station. bikes_available || 0}</span>
                    </div>
                    <div className="popup-stat">
                      <span className="popup-icon">🅿️</span>
                      <span className="popup-label">Docks: </span>
                      <span className="popup-value">{station.docks_available || 0}</span>
                    </div>
                  </div>

                  {station.distance && (
                    <p className="popup-distance">📏 {station.distance_km} km away</p>
                  )}

                  <button
                    onClick={() => getDirections(station)}
                    className="btn btn-primary btn-sm popup-btn"
                  >
                    🗺️ Get Directions
                  </button>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Map Legend */}
      <div className="map-legend">
        <h4>🎨 Map Legend: </h4>
        <div className="legend-items">
          <div className="legend-item">
            <span className="legend-marker green">●</span>
            <span>High Availability (&gt;50%)</span>
          </div>
          <div className="legend-item">
            <span className="legend-marker yellow">●</span>
            <span>Medium Availability (20-50%)</span>
          </div>
          <div className="legend-item">
            <span className="legend-marker red">●</span>
            <span>Low Availability (&lt;20%)</span>
          </div>
          <div className="legend-item">
            <span className="legend-marker blue">●</span>
            <span>Your Location</span>
          </div>
        </div>
      </div>

      {/* Station List */}
      <div className="stations-list">
        <h2>All Stations ({stations.length})</h2>
        <div className="stations-grid">
          {stations.slice(0, 12).map((station) => (
            <div key={station.id} className="station-card">
              <h3>{station.name}</h3>
              <p className="station-address">{station.address}</p>

              <div className="station-stats">
                <div className="stat">
                  <span className="stat-label">🚲 Bikes</span>
                  <span className="stat-value">{station. bikes_available || 0}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">🅿️ Docks</span>
                  <span className="stat-value">{station.docks_available || 0}</span>
                </div>
                {station.distance && (
                  <div className="stat">
                    <span className="stat-label">📏 Distance</span>
                    <span className="stat-value">{station.distance_km} km</span>
                  </div>
                )}
              </div>

              <div className="station-actions">
                <button
                  onClick={() => centerOnStation(station)}
                  className="btn btn-secondary btn-sm"
                >
                  View on Map
                </button>
                <button onClick={() => getDirections(station)} className="btn btn-outline btn-sm">
                  Directions
                </button>
              </div>

              <div className={`station-status ${station.status}`}>
                {station.status === 'active' ? '✓ Active' : '✗ Inactive'}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BikeStations;