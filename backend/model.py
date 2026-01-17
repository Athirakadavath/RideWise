import pickle
import numpy as np
import os
from datetime import datetime

# Load models at module level
DAILY_MODEL = None
HOURLY_MODEL = None

def load_models():
    """Load both models when module is imported"""
    global DAILY_MODEL, HOURLY_MODEL

    # Updated model paths
    daily_model_path = 'models/xgb_day_new.pkl'
    hourly_model_path = 'models/xgb_hour_new.pkl'

    if os. path.exists(daily_model_path):
        with open(daily_model_path, 'rb') as f:
            DAILY_MODEL = pickle.load(f)
        print(f"✓ Daily model loaded from {daily_model_path}")
        if hasattr(DAILY_MODEL, 'n_features_in_'):
            print(f"  Expects {DAILY_MODEL. n_features_in_} features")
    else:
        raise FileNotFoundError(f"❌ Daily model not found at {daily_model_path}")

    if os.path.exists(hourly_model_path):
        with open(hourly_model_path, 'rb') as f:
            HOURLY_MODEL = pickle.load(f)
        print(f"✓ Hourly model loaded from {hourly_model_path}")
        if hasattr(HOURLY_MODEL, 'n_features_in_'):
            print(f"  Expects {HOURLY_MODEL. n_features_in_} features")
    else:
        raise FileNotFoundError(f"❌ Hourly model not found at {hourly_model_path}")

load_models()

def engineer_daily_features(features_dict):
    """
    Daily model features (19 features, excludes 'cnt'):
    EXACT ORDER from your new dataset:
    atemp, day_sin, holiday, hum, humidity_windspeed, is_weekend,
    mnth_cos, mnth_sin, season_4, temp, temp_comfort, temp_humidity,
    temp_squared, weather_temp_interaction, weekday_cos, weekday_sin,
    windspeed, workingday, yr
    """

    # Extract base features
    yr = int(features_dict.get('yr', 1))
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

    # Get day from date if provided, otherwise use default
    if 'date' in features_dict:
        try:
            date_obj = datetime.strptime(features_dict['date'], '%Y-%m-%d')
            day = date_obj.day
        except:
            day = 15  # Default to mid-month
    else:
        day = 15

    # Binary features
    is_weekend = 1 if weekday in [0, 6] else 0  # Sunday=0, Saturday=6

    # Cyclical encoding
    mnth_sin = np.sin(2 * np.pi * mnth / 12)
    mnth_cos = np.cos(2 * np.pi * mnth / 12)
    weekday_sin = np.sin(2 * np.pi * weekday / 7)
    weekday_cos = np.cos(2 * np.pi * weekday / 7)
    day_sin = np.sin(2 * np.pi * day / 31)

    # One-hot encoding for season (only season_4)
    season_4 = 1 if season == 4 else 0

    # Squared features
    temp_squared = temp ** 2

    # Interaction features
    temp_comfort = temp * atemp
    humidity_windspeed = hum * windspeed
    temp_humidity = temp * hum
    weather_temp_interaction = weathersit * temp

    # Assemble in EXACT order from your new dataset
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
    Hourly model features (24 features, excludes 'cnt'):
    EXACT ORDER from your new dataset:
    atemp, day_sin, holiday, hr_cos, hr_sin, hum, humidity_windspeed,
    is_peak_hour, is_weekend, mnth_cos, mnth_sin, season_4, temp,
    temp_comfort, temp_humidity, temp_squared, time_of_day_evening,
    time_of_day_morning, weathersit_3, weekday_cos, weekday_sin,
    windspeed, workingday, yr
    """

    # Extract base features
    yr = int(features_dict.get('yr', 1))
    holiday = int(features_dict.get('holiday', 0))
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
            date_obj = datetime. strptime(features_dict['date'], '%Y-%m-%d')
            day = date_obj.day
        except:
            day = 15
    else:
        day = 15

    # Binary features
    is_weekend = 1 if weekday in [0, 6] else 0  # Sunday=0, Saturday=6
    is_peak_hour = 1 if hr in [7, 8, 9, 17, 18, 19] else 0

    # Time of day categories
    time_of_day_morning = 1 if 6 <= hr < 12 else 0
    time_of_day_evening = 1 if 18 <= hr < 24 else 0

    # Cyclical encoding
    hr_sin = np.sin(2 * np.pi * hr / 24)
    hr_cos = np.cos(2 * np.pi * hr / 24)
    weekday_sin = np.sin(2 * np. pi * weekday / 7)
    weekday_cos = np.cos(2 * np. pi * weekday / 7)
    mnth_sin = np.sin(2 * np. pi * mnth / 12)
    mnth_cos = np.cos(2 * np. pi * mnth / 12)
    day_sin = np. sin(2 * np.pi * day / 31)

    # One-hot encoding for season (only season_4)
    season_4 = 1 if season == 4 else 0

    # One-hot encoding for weather (only weathersit_3)
    weathersit_3 = 1 if weathersit == 3 else 0

    # Squared features
    temp_squared = temp ** 2

    # Interaction features
    temp_comfort = temp * atemp
    humidity_windspeed = hum * windspeed
    temp_humidity = temp * hum

    # Assemble in EXACT order from your new dataset
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
    """Predict daily bike rentals"""
    if DAILY_MODEL is None:
        raise RuntimeError("Daily model not loaded")

    try:
        features = engineer_daily_features(features_dict)
        print(f"Daily prediction - features shape:  {features.shape}")

        prediction = DAILY_MODEL.predict(features)[0]
        result = max(0, float(prediction))

        print(f"Daily prediction result: {int(result)} bikes")
        return result

    except Exception as e:
        print(f"Daily prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

def predict_hourly(features_dict):
    """Predict hourly bike rentals"""
    if HOURLY_MODEL is None:
        raise RuntimeError("Hourly model not loaded")

    try:
        features = engineer_hourly_features(features_dict)
        print(f"Hourly prediction - features shape: {features.shape}")

        prediction = HOURLY_MODEL. predict(features)[0]
        result = max(0, float(prediction))

        print(f"Hourly prediction result: {int(result)} bikes")
        return result

    except Exception as e:
        print(f"Hourly prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise