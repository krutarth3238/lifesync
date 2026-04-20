# LifeSync — AI Productivity Command Center

LifeSync is a local CLI productivity assistant that connects to Google Calendar, Gmail, Google Sheets, and Google Maps to help you check your schedule, review emails, log tasks, and estimate commute times.

## Features

- View calendar events for a given day
- Read unread Gmail messages
- Log tasks into Google Sheets
- Estimate driving time and distance with Google Maps
- Simple terminal-based interface powered by Rich

## Tech Stack

- Python
- Google Calendar API
- Gmail API
- Google Sheets API
- Google Maps Distance Matrix API
- Gemini / AI assistant layer
- Rich
- python-dotenv

## Project Structure

```text
lifesync/
├── main.py
├── requirements.txt
├── .env
├── credentials.json
├── agent/
│   └── gemini_agent.py
├── services/
│   ├── calendar_service.py
│   ├── gmail_service.py
│   ├── sheets_service.py
│   └── maps_service.py
└── README.md
