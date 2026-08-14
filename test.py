from dotenv import load_dotenv
load_dotenv()

import os
from sdk.api_tracker import APITracker

tracker = APITracker(
    project="Local-Test",
    backend_url=os.getenv("TRACKER_BACKEND_URL", "http://localhost:8000"),
    gemini_api_key=os.getenv("GEMINI_API_KEY"),
)

response = tracker.gemini.generate(
    model="gemini-2.5-flash",
    contents="Get me info about Sarvam"
)

print(response.text)