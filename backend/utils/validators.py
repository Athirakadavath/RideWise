import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""

def validate_prediction_input(data, prediction_type='daily'):
    """Validate prediction input"""
    required_fields = ['season', 'mnth', 'weekday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'workingday']

    if prediction_type == 'hourly':
        required_fields. append('hr')

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    validations = {
        'season':  (1, 4),
        'mnth': (1, 12),
        'weekday': (0, 6),
        'weathersit': (1, 4),
        'temp': (0, 1),
        'atemp': (0, 1),
        'hum': (0, 1),
        'windspeed': (0, 1),
        'workingday': (0, 1),
    }

    if prediction_type == 'hourly':
        validations['hr'] = (0, 23)

    for field, (min_val, max_val) in validations.items():
        try:
            value = float(data[field])
            if value < min_val or value > max_val:
                return False, f"{field} must be between {min_val} and {max_val}"
        except (ValueError, TypeError):
            return False, f"{field} must be a number"

    return True, ""