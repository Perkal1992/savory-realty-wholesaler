import streamlit as st
import pandas as pd
import requests
import os
from config import GOOGLE_MAPS_API_KEY

st.set_page_config(page_title="Savory Realty Investments — Wholesaling Dashboard", layout="wide")

st.title("🏘️ Savory Realty Investments")
st.markdown("Upload a CSV of property addresses. We'll enrich them with location data and generate Google Maps + Street View links.")

uploaded_file = st.file_uploader("📁 Upload CSV", type=["csv"])

def geocode_address(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        if result["status"] == "OK":
            location = result["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "Address" not in df.columns:
        st.error("❌ Your CSV must contain a column named 'Address'")
    else:
        with st.spinner("Geocoding addresses..."):
            latitudes, longitudes, maps_links, street_views = [], [], [], []

            for address in df["Address"]:
                lat, lng = geocode_address(address)
                if lat and lng:
                    latitudes.append(lat)
                    longitudes.append(lng)
                    maps_links.append(f"https://www.google.com/maps/search/?api=1&query={lat},{lng}")
                    street_views.append(f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lng}")
                else:
                    latitudes.append("")
                    longitudes.append("")
                    maps_links.append("")
                    street_views.append("")

            df["Latitude"] = latitudes
            df["Longitude"] = longitudes
            df["Google Maps"] = maps_links
            df["Street View"] = street_views

        st.success("✅ Processing complete")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Processed CSV", csv, file_name="processed_properties.csv", mime="text/csv")
