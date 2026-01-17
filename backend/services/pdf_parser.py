import re
import PyPDF2
from datetime import datetime


def extract_data_from_pdf(pdf_path):
    """
    Parse PDF and return a COMPLETE feature dictionary
    compatible with DAILY and HOURLY ML models.
    """

    try:
        # --------------------------------------------------
        # READ PDF
        # --------------------------------------------------
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        print("=" * 60)
        print("RAW PDF TEXT")
        print("=" * 60)
        print(text)
        print("=" * 60)

        if not text.strip():
            print("❌ PDF has no extractable text")
            return None

        text_lower = text.lower()
        data = {}

        # --------------------------------------------------
        # DATE (FIXED – HANDLES SPACES AROUND DASH)
        # --------------------------------------------------
        date_match = re.search(
            r"date\s*[:\-]?\s*(\d{4}\s*[-/]\s*\d{2}\s*[-/]\s*\d{2}|\d{2}\s*[-/]\s*\d{2}\s*[-/]\s*\d{4})",
            text_lower
        )

        if not date_match:
            print("❌ Date is mandatory but not found")
            return None

        raw_date = date_match.group(1)
        raw_date = re.sub(r"\s+", "", raw_date)  # remove spaces

        try:
            date_obj = datetime.strptime(raw_date, "%Y-%m-%d")
        except ValueError:
            date_obj = datetime.strptime(raw_date, "%d-%m-%Y")

        data["date"] = date_obj.strftime("%Y-%m-%d")

        # --------------------------------------------------
        # HOUR (OPTIONAL BUT REQUIRED FOR HOURLY MODEL)
        # --------------------------------------------------
        hr_match = re.search(r"hour\s*[:\-]?\s*(\d{1,2})", text_lower)
        data["hr"] = int(hr_match.group(1)) if hr_match else 12

        # --------------------------------------------------
        # WEATHER
        # --------------------------------------------------
        weather_match = re.search(r"weather\s*[:\-]?\s*(\d)", text_lower)
        data["weathersit"] = int(weather_match.group(1)) if weather_match else 1

        # --------------------------------------------------
        # TEMPERATURE (MANDATORY)
        # --------------------------------------------------
        temp_match = re.search(r"temperature\s*[:\-]?\s*([\d.]+)", text_lower)
        if not temp_match:
            print("❌ Temperature is mandatory")
            return None

        temp = float(temp_match.group(1))
        data["temp"] = temp

        # --------------------------------------------------
        # HUMIDITY
        # --------------------------------------------------
        hum_match = re.search(r"humidity\s*[:\-]?\s*([\d.]+)", text_lower)
        hum = float(hum_match.group(1)) if hum_match else 0.6
        data["hum"] = hum

        # --------------------------------------------------
        # WIND SPEED
        # --------------------------------------------------
        wind_match = re.search(r"wind\s*speed\s*[:\-]?\s*([\d.]+)", text_lower)
        wind = float(wind_match.group(1)) if wind_match else 0.2
        data["windspeed"] = wind

        # --------------------------------------------------
        # WORKING DAY
        # --------------------------------------------------
        wd_match = re.search(r"working\s*day\s*[:\-]?\s*(\d)", text_lower)
        data["workingday"] = int(wd_match.group(1)) if wd_match else 1

        # --------------------------------------------------
        # HOLIDAY
        # --------------------------------------------------
        holiday_match = re.search(r"holiday\s*[:\-]?\s*(\d)", text_lower)
        data["holiday"] = int(holiday_match.group(1)) if holiday_match else 0

        # --------------------------------------------------
        # DERIVED DATE FEATURES (MODEL CRITICAL)
        # --------------------------------------------------
        month = date_obj.month
        weekday = (date_obj.weekday() + 1) % 7

        if month in [3, 4, 5]:
            season = 2
        elif month in [6, 7, 8]:
            season = 3
        elif month in [9, 10, 11]:
            season = 4
        else:
            season = 1

        data.update({
            "mnth": month,
            "weekday": weekday,
            "season": season,
            "yr": 1 if date_obj.year >= 2012 else 0,
            "atemp": data["temp"],  # model expects atemp
        })

        # --------------------------------------------------
        # FINAL VALIDATION
        # --------------------------------------------------
        REQUIRED_FIELDS = [
            "temp", "atemp", "hum", "windspeed",
            "season", "mnth", "weekday",
            "workingday", "weathersit",
            "holiday", "yr"
        ]

        missing = [f for f in REQUIRED_FIELDS if f not in data]
        if missing:
            print("❌ Missing required fields:", missing)
            return None

        # --------------------------------------------------
        # DEBUG OUTPUT
        # --------------------------------------------------
        print("=" * 60)
        print("✅ FINAL FEATURE DICTIONARY (MODEL INPUT)")
        print("=" * 60)
        for k, v in sorted(data.items()):
            print(f"{k:12} : {v}")

        return data

    except Exception as e:
        print("❌ PDF parsing error:", str(e))
        import traceback
        traceback.print_exc()
        return None
