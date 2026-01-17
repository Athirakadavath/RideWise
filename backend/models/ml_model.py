import pickle
import numpy as np
from datetime import datetime
from config import Config
import os

# Global model variables
DAILY_MODEL = None
HOURLY_MODEL = None

def load_models():
    """Load ML models"""
    global DAILY_MODEL, HOURLY_MODEL

    try:
        # Load daily model
        if os.path.exists(Config. DAILY_MODEL_PATH):
            with open(Config.DAILY_MODEL_PATH, 'rb') as f:
                DAILY_MODEL = pickle.load(f)
            print(f"✓ Daily model loaded:  {Config.DAILY_MODEL_PATH}")
            if hasattr(DAILY_MODEL, 'n_features_in_'):
                print(f"  Expected features: {DAILY_MODEL. n_features_in_}")
        else:
            print(f"⚠ Daily model not found at {Config.DAILY_MODEL_PATH}")

        # Load hourly model
        if os. path.exists(Config.HOURLY_MODEL_PATH):
            with open(Config.HOURLY_MODEL_PATH, 'rb') as f:
                HOURLY_MODEL = pickle.load(f)
            print(f"✓ Hourly model loaded: {Config.HOURLY_MODEL_PATH}")
            if hasattr(HOURLY_MODEL, 'n_features_in_'):
                print(f"  Expected features: {HOURLY_MODEL.n_features_in_}")
        else:
            print(f"⚠ Hourly model not found at {Config.HOURLY_MODEL_PATH}")

    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        raise

# Load models on module import
load_models()

def engineer_daily_features(features_dict):
    """
    Engineer features for daily prediction
    Order: atemp, day_sin, holiday, hum, humidity_windspeed, is_weekend,
           mnth_cos, mnth_sin, season_4, temp, temp_comfort, temp_humidity,
           temp_squared, weather_temp_interaction, weekday_cos, weekday_sin,
           windspeed, workingday, yr
    """
    # Extract base features
    yr = int(features_dict. get('yr', 1))
    holiday = int(features_dict.get('holiday', 0))
    temp = float(features_dict['temp'])
    atemp = float(features_dict['atemp'])
    hum = float(features_dict['hum'])
    windspeed = float(features_dict['windspeed'])
    season = int(features_dict['season'])
    mnth = int(features_dict['mnth'])
    weekday = int(features_dict['weekday'])
    workingday = int(features_dict['workingday'])
    weathersit = int(features_dict['weathersit'])

    # Get day from date if provided
    if 'date' in features_dict:
        try:
            date_obj = datetime.strptime(features_dict['date'], '%Y-%m-%d')
            day = date_obj.day
        except:
            day = 15
    else:
        day = 15

    # Binary features
    is_weekend = 1 if weekday in [0, 6] else 0

    # Cyclical encoding
    mnth_sin = np.sin(2 * np.pi * mnth / 12)
    mnth_cos = np.cos(2 * np.pi * mnth / 12)
    weekday_sin = np.sin(2 * np.pi * weekday / 7)
    weekday_cos = np.cos(2 * np.pi * weekday / 7)
    day_sin = np.sin(2 * np.pi * day / 31)

    # One-hot encoding
    season_4 = 1 if season == 4 else 0

    # Squared features
    temp_squared = temp ** 2

    # Interaction features
    temp_comfort = temp * atemp
    humidity_windspeed = hum * windspeed
    temp_humidity = temp * hum
    weather_temp_interaction = weathersit * temp

    # Assemble features in exact order
    return np.array([[
        atemp,                          # 0
        day_sin,                        # 1
        holiday,                        # 2
        hum,                            # 3
        humidity_windspeed,             # 4
        is_weekend,                     # 5
        mnth_cos,                       # 6
        mnth_sin,                       # 7
        season_4,                       # 8
        temp,                           # 9
        temp_comfort,                   # 10
        temp_humidity,                  # 11
        temp_squared,                   # 12
        weather_temp_interaction,       # 13
        weekday_cos,                    # 14
        weekday_sin,                    # 15
        windspeed,                      # 16
        workingday,                     # 17
        yr,                             # 18
    ]])

def engineer_hourly_features(features_dict):
    """
    Engineer features for hourly prediction
    Order: atemp, day_sin, holiday, hr_cos, hr_sin, hum, humidity_windspeed,
           is_peak_hour, is_weekend, mnth_cos, mnth_sin, season_4, temp,
           temp_comfort, temp_humidity, temp_squared, time_of_day_evening,
           time_of_day_morning, weathersit_3, weekday_cos, weekday_sin,
           windspeed, workingday, yr
    """
    # Extract base features
    yr = int(features_dict.get('yr', 1))
    holiday = int(features_dict. get('holiday', 0))
    workingday = int(features_dict['workingday'])
    temp = float(features_dict['temp'])
    atemp = float(features_dict['atemp'])
    hum = float(features_dict['hum'])
    windspeed = float(features_dict['windspeed'])
    season = int(features_dict['season'])
    mnth = int(features_dict['mnth'])
    weekday = int(features_dict['weekday'])
    weathersit = int(features_dict['weathersit'])
    hr = int(features_dict. get('hr', 12))

    # Get day from date if provided
    if 'date' in features_dict:
        try:
            date_obj = datetime.strptime(features_dict['date'], '%Y-%m-%d')
            day = date_obj.day
        except:
            day = 15
    else:
        day = 15

    # Binary features
    is_weekend = 1 if weekday in [0, 6] else 0
    is_peak_hour = 1 if hr in [7, 8, 9, 17, 18, 19] else 0

    # Time of day categories
    time_of_day_morning = 1 if 6 <= hr < 12 else 0
    time_of_day_evening = 1 if 18 <= hr < 24 else 0

    # Cyclical encoding
    hr_sin = np.sin(2 * np.pi * hr / 24)
    hr_cos = np.cos(2 * np. pi * hr / 24)
    weekday_sin = np.sin(2 * np.pi * weekday / 7)
    weekday_cos = np.cos(2 * np.pi * weekday / 7)
    mnth_sin = np.sin(2 * np.pi * mnth / 12)
    mnth_cos = np.cos(2 * np.pi * mnth / 12)
    day_sin = np.sin(2 * np.pi * day / 31)

    # One-hot encoding
    season_4 = 1 if season == 4 else 0
    weathersit_3 = 1 if weathersit == 3 else 0

    # Squared features
    temp_squared = temp ** 2

    # Interaction features
    temp_comfort = temp * atemp
    humidity_windspeed = hum * windspeed
    temp_humidity = temp * hum

    # Assemble features in exact order
    return np.array([[
        atemp,                          # 0
        day_sin,                        # 1
        holiday,                        # 2
        hr_cos,                         # 3
        hr_sin,                         # 4
        hum,                            # 5
        humidity_windspeed,             # 6
        is_peak_hour,                   # 7
        is_weekend,                     # 8
        mnth_cos,                       # 9
        mnth_sin,                       # 10
        season_4,                       # 11
        temp,                           # 12
        temp_comfort,                   # 13
        temp_humidity,                  # 14
        temp_squared,                   # 15
        time_of_day_evening,            # 16
        time_of_day_morning,            # 17
        weathersit_3,                   # 18
        weekday_cos,                    # 19
        weekday_sin,                    # 20
        windspeed,                      # 21
        workingday,                     # 22
        yr,                             # 23
    ]])

def predict_daily(features_dict):
    """Make daily prediction"""
    if DAILY_MODEL is None:
        raise RuntimeError("Daily model not loaded")

    try:
        features = engineer_daily_features(features_dict)
        prediction = DAILY_MODEL.predict(features)[0]

        # Apply weather penalty
        weathersit = int(features_dict['weathersit'])
        weather_penalty = {1: 1.0, 2: 0.85, 3: 0.50, 4: 0.25}
        penalty = weather_penalty.get(weathersit, 1.0)
        result = prediction * penalty
        result = max(0, float(result))

        print(f"Daily prediction: {int(result)} bikes (weather penalty: {penalty}x)")
        return result

    except Exception as e:
        print(f"Daily prediction error: {str(e)}")
        raise

def predict_hourly(features_dict):
    """Make hourly prediction"""
    if HOURLY_MODEL is None:
        raise RuntimeError("Hourly model not loaded")

    try:
        features = engineer_hourly_features(features_dict)
        prediction = HOURLY_MODEL.predict(features)[0]

        # Apply weather penalty
        weathersit = int(features_dict['weathersit'])
        weather_penalty = {1: 1.0, 2: 0.85, 3: 0.50, 4: 0.25}
        penalty = weather_penalty.get(weathersit, 1.0)
        result = prediction * penalty
        result = max(0, float(result))

        print(f"Hourly prediction: {int(result)} bikes (weather penalty: {penalty}x)")
        return result

    except Exception as e:
        print(f"Hourly prediction error: {str(e)}")
        raise