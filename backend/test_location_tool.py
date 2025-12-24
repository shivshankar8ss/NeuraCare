# import googlemaps
# from backend.config import GOOGLE_MAPS_API_KEY

# gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# def find_nearby_therapists_by_location(location: str) -> str:
#     geocode_result = gmaps.geocode(location)
#     lat_lng = geocode_result[0]['geometry']['location']
#     lat, lng = lat_lng['lat'], lat_lng['lng']
#     places_result = gmaps.places_nearby(
#             location=(lat, lng),
#             radius=5000,
#             keyword="Psychotherapist"
#         )
#     output = [f"Therapists near {location}:"]
#     top_results = places_result['results'][:5]
#     for place in top_results:
#             name = place.get("name", "Unknown")
#             address = place.get("vicinity", "Address not available")
#             details = gmaps.place(place_id=place["place_id"], fields=["formatted_phone_number"])
#             phone = details.get("result", {}).get("formatted_phone_number", "Phone not available")

#             output.append(f"- {name} | {address} | {phone}")
   
#     return "\n".join(output)


# settnng geoapi since google map api doesnt work
from langchain_core.tools import tool
from geopy.geocoders import Nominatim

@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds therapists near a location using OpenStreetMap (free, no billing).
    """
    try:
        geolocator = Nominatim(user_agent="mentme-app")
        geo = geolocator.geocode(location)

        if not geo:
            return f"I couldn't find the location '{location}'. Please try a nearby city."
        lat, lon = geo.latitude, geo.longitude
        return (
            f"I found the location for {location}.\n"
            f"You can search for nearby therapists using:\n"
            f"https://www.openstreetmap.org/#map=14/{lat}/{lon}\n\n"
            "You may also search on Google using 'therapist near me'."
        )
    except Exception:
        return (
            "I'm unable to look up nearby therapists right now, "
            "but I can still help you think through next steps or coping strategies."
        )
