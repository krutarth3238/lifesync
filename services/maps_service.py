import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

def get_commute_time(origin: str, destination: str) -> dict:
    try:
        api_key = os.getenv("MAPS_API_KEY")

        if not api_key:
            return {"error": "Maps API key not found"}

        gmaps = googlemaps.Client(key=api_key)

        result = gmaps.distance_matrix(
            origins=[origin],
            destinations=[destination],
            mode="driving"
        )

        element = result['rows'][0]['elements'][0]

        if element['status'] != 'OK':
            return {"error": "Route not found"}

        return {
            "duration": element['duration']['text'],
            "distance": element['distance']['text'],
            "origin": origin,
            "destination": destination
        }

    except Exception as ex:
        return {"error": str(ex), "service": "Google Maps"}