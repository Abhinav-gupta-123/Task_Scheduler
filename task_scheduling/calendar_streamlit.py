import streamlit as st
import requests
from googleapiclient.discovery import build
from google_auth import get_google_credentials
from datetime import datetime, date, time

st.title("📅 Google Calendar Event Scheduler")

# Ensure token is not deleted by Streamlit refresh
if "google_creds" not in st.session_state:
    try:
        creds = get_google_credentials()
        st.session_state.google_creds = creds
        service = build("calendar", "v3", credentials=creds)
        st.session_state.google_service = service
        st.success("✅ Successfully authenticated with Google Calendar!")
    except Exception as e:
        st.error(f"❌ Authentication failed: {e}")
        st.stop()
else:
    creds = st.session_state.google_creds
    service = st.session_state.google_service

# Set defaults
current_date = date.today()
current_time = datetime.now().time()

# Input fields
event_title = st.text_input("Event Title", "Meeting with Team")
event_date = st.date_input("Event Date", value=current_date)
event_time = st.time_input("Event Time", value=current_time)

# Function to create an event
def create_event():
    try:
        start_datetime = datetime.combine(event_date, event_time)
        event = {
            "summary": event_title,
            "start": {"dateTime": start_datetime.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": start_datetime.isoformat(), "timeZone": "Asia/Kolkata"},
        }

        event = service.events().insert(calendarId="primary", body=event).execute()
        st.success(f"✅ Event Created: [🔗 View on Calendar]({event.get('htmlLink')})")
    except Exception as e:
        st.error(f"❌ Failed to create event: {e}")

# Schedule event button
if st.button("Schedule Event"):
    create_event()

st.divider()

# Fetch and display upcoming events from FastAPI
st.subheader("📌 Upcoming Events")

try:
    response = requests.get("http://127.0.0.1:8000/upcoming_events/")
    
    if response.status_code == 200:
        data = response.json()

        if "upcoming_events" in data and len(data["upcoming_events"]) > 0:
            for event in data["upcoming_events"]:
                title = event.get("summary", "No Title")  # FIXED: Use 'summary' instead of 'title'
                start_time = event["start"].get("dateTime", event["start"].get("date", "Unknown Date"))  # Handle both dateTime and date
                link = event.get("htmlLink", "#")  # Provide a default if link is missing

                st.markdown(f"### {title}")
                st.markdown(f"**📅 Date & Time:** {start_time}")
                st.markdown(f"[🔗 View Event]({link})")
                st.divider()
        else:
            st.warning("🚫 No upcoming events found.")
    else:
        st.error(f"❌ Failed to fetch events: Server responded with {response.status_code}")
except Exception as e:
    st.error(f"❌ Failed to fetch events: {e}")
