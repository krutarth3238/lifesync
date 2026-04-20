from services.calendar_service import get_calendar_events
from services.gmail_service import get_unread_emails
from services.sheets_service import append_to_sheet
from services.maps_service import get_commute_time

def build_agent():
    return None

def ask_agent(_, user_input: str) -> str:
    user_input = user_input.lower()

    try:
        if "calendar" in user_input:
            return str(get_calendar_events())

        elif "email" in user_input:
            return str(get_unread_emails())

        elif "task" in user_input:
            return str(append_to_sheet("Sample Task", "High"))

        elif "drive" in user_input or "commute" in user_input:
            return str(get_commute_time("Mumbai", "Pune"))

        else:
            return "I'm your productivity assistant. Ask about calendar, emails, tasks, or commute."

    except Exception as e:
        return f"Error: {str(e)}"