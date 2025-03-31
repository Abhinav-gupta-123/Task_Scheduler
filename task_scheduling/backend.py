from fastapi import FastAPI
from googleapiclient.discovery import build
from google_auth import get_google_credentials
from datetime import datetime, timezone

app = FastAPI()

# ✅ Test if FastAPI is running
@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

# ✅ Fetch upcoming Google Calendar events
@app.get("/upcoming_events/")
def read_upcoming_events():
    try:
        creds = get_google_credentials()
        service = build("calendar", "v3", credentials=creds)

        now = datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(calendarId="primary", timeMin=now, maxResults=5, singleEvents=True, orderBy="startTime")
            .execute()
        )
        events = events_result.get("items", [])

        upcoming_events = []
        for event in events:
            event_data = {
                "summary": event.get("summary", "No Title"),
                "start": event.get("start", {}),
                "end": event.get("end", {}),
                "htmlLink": event.get("htmlLink", "#"),
            }
            upcoming_events.append(event_data)

        return {"upcoming_events": upcoming_events}

    except Exception as e:
        return {"error": str(e)}
