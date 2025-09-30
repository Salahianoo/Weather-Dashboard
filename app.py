import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Weather Dashboard", page_icon="🌦️", layout="wide")

st.title("🌦️ Weather Forecast Dashboard")

# --- Input: اسم المدينة ---
city = st.text_input("Enter city name:", "Amman")

# --- API Key (ضع API KEY الخاص بك) ---
API_KEY = "322e21815f54bf3a5debc8c4be45acd0"
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url).json()

    if "list" in response:
        forecast = response["list"]

        # --- تحويل ل DataFrame ---
        data = []
        for f in forecast:
            data.append({
                "datetime": datetime.fromtimestamp(f["dt"]),
                "temp": f["main"]["temp"],
                "feels_like": f["main"]["feels_like"],
                "humidity": f["main"]["humidity"],
                "weather": f["weather"][0]["description"].title()
            })

        df = pd.DataFrame(data)

        # --- استخراج بيانات اليوم الحالي ---
        current = df.iloc[0]

        # --- بطاقات ملخص ---
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temperature", f"{current['temp']:.1f} °C", f"Feels like {current['feels_like']:.1f} °C")
        col2.metric("💧 Humidity", f"{current['humidity']} %")
        col3.metric("⛅ Condition", current["weather"])

        # --- جدول ---
        st.subheader(f"Weather Forecast for {city}")
        st.dataframe(df)

        # --- رسم بياني للحرارة ---
        st.subheader("Temperature Trend (Next Days)")
        fig, ax = plt.subplots(figsize=(6,3))
        ax.plot(df["datetime"], df["temp"], marker="o", label="Temperature (°C)")
        ax.plot(df["datetime"], df["feels_like"], marker="x", linestyle="--", label="Feels Like (°C)")
        ax.set_ylabel("°C")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        # --- رطوبة ---
        st.subheader("Humidity Trend")
        fig2, ax2 = plt.subplots(figsize=(6,3))
        ax2.bar(df["datetime"], df["humidity"], color="skyblue")
        ax2.set_ylabel("% Humidity")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig2)

    else:
        st.error("❌ Failed to fetch weather data. Check city name or API key.")

except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")
