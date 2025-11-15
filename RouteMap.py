import googlemaps
import folium
import webbrowser
from datetime import datetime
from googlemaps.convert import decode_polyline

# IMPORTANT: Replace the placeholder API key with your actual, restricted key.
# Your key must have the Directions API and Places API enabled.
API_KEY = "AIzaSyBJvLf7ELmjeX6KSmaGHHi2-Ks1QBkWWR0" 
gmaps = googlemaps.Client(key=API_KEY)


def find_restaurants_along_route(origin, destination, radius=1500, max_results=5):
    """
    Helper function: Finds restaurants along the route using the Places API.
    """
    # Define a temporary gmaps client here (if you rely on the API key being in a specific location)
    # or rely on the global gmaps object. For simplicity, we'll assume the global client is used 
    # and the API key is passed via the gmaps object.
    
    directions = gmaps.directions(origin, destination, mode="driving")
    if not directions:
        return []

    steps = directions[0]['legs'][0]['steps']
    # Select only the start point of each step for searching
    route_points = [(step['start_location']['lat'], step['start_location']['lng']) for step in steps]

    all_restaurants = []
    seen_places = set()
    
    # Iterate through selected route points and search for nearby restaurants
    for lat, lng in route_points:
        places_result = gmaps.places_nearby(
            location=(lat, lng), 
            radius=radius,
            type="restaurant"
        )
        
        for place in places_result.get('results', []):
            pid = place['place_id']
            if pid not in seen_places:
                seen_places.add(pid)
                all_restaurants.append({
                    'name': place['name'],
                    'address': place.get('vicinity', ''),
                    'rating': place.get('rating', 'N/A'),
                    'location': place['geometry']['location']
                })
            if len(all_restaurants) >= max_results:
                break
        if len(all_restaurants) >= max_results:
            break
            
    return all_restaurants
import folium
import webbrowser
from datetime import datetime

# Example: Data structure to hold route condition info
route_conditions = [
    {"lat": 17.412, "lng": 78.128, "type": "damaged", "desc": "Road damaged due to potholes"},
    {"lat": 17.415, "lng": 78.132, "type": "construction", "desc": "Construction work: single lane traffic"},
    # Add more entries as you need with lat/lng and info
]

def add_route_condition_markers(map_obj, route_conditions):
    for cond in route_conditions:
        if cond["type"] == "damaged":
            color = 'red'
            icon = 'exclamation-triangle'
        elif cond["type"] == "construction":
            color = 'orange'
            icon = 'wrench'
        else:
            color = 'gray'
            icon = 'info-sign'
        folium.Marker(
            location=[cond["lat"], cond["lng"]],
            popup=f"<b>{cond['type'].capitalize()}</b><br>{cond['desc']}",
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(map_obj)

def generateroutewithconditions(origin, destination, route_conditions, gmaps):
    directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now(), alternatives=True)
    geocode_origin = gmaps.geocode(origin)[0]["geometry"]["location"]
    geocode_dest = gmaps.geocode(destination)[0]["geometry"]["location"]
    midlat = (geocode_origin["lat"] + geocode_dest["lat"]) / 2
    midlng = (geocode_origin["lng"] + geocode_dest["lng"]) / 2
    map_route = folium.Map(location=[midlat, midlng], zoom_start=12)

    # Polyline drawing (route)
    steps = directions_result[0]['legs'][0]['steps']
    route_points = []
    for step in steps:
        lat = step['start_location']['lat']
        lng = step['start_location']['lng']
        route_points.append([lat, lng])
    folium.PolyLine(route_points, color="blue", weight=4.5, opacity=0.7).add_to(map_route)

    # Add condition markers
    add_route_condition_markers(map_route, route_conditions)

    map_file = "routemap_with_conditions.html"
    map_route.save(map_file)
    webbrowser.open(map_file)

# Paste this at the main entry:
if __name__ == "_main_":
    import googlemaps  # Import inside main for copy-paste use
    API_KEY = 'YOUR-API-KEY-HERE'
    gmaps = googlemaps.Client(key=API_KEY)
    origin = input("Enter your start location: ")
    destination = input("Enter your destination: ")
    generateroutewithconditions(origin, destination, route_conditions, gmaps)
# ----------------------------------------------------------------------
# NEW FUNCTION - Includes Traffic and Restaurants
# ----------------------------------------------------------------------
def generate_route_with_traffic_and_restaurants(origin, destination, openmap=True):
    """
    Generates a Folium map showing the routes (with traffic-aware duration in tooltips) 
    and restaurant markers, including distinct Origin and Destination markers.
    """
    # Request directions, ensuring departure_time is set to get 'duration_in_traffic'
    directions_result = gmaps.directions(
        origin, 
        destination, 
        mode="driving", 
        departure_time=datetime.now(), # This enables traffic calculation
        alternatives=True
    )
    
    if not directions_result:
        print("No route found.")
        return None, [], []

    # Get geocoded location data for O & D
    geocode_origin = gmaps.geocode(origin)[0]['geometry']['location']
    geocode_dest = gmaps.geocode(destination)[0]['geometry']['location']
    mid_lat = (geocode_origin['lat'] + geocode_dest['lat'])/2
    mid_lng = (geocode_origin['lng'] + geocode_dest['lng'])/2
    
    # Create the base map
    maproute = folium.Map(location=[mid_lat, mid_lng], zoom_start=12)

    # --- ADDED: Origin and Destination Markers ---
    # Origin Marker
    folium.Marker(
        [geocode_origin['lat'], geocode_origin['lng']],
        popup=f"<b>Origin:</b> {origin}",
        icon=folium.Icon(color='darkblue', icon='circle', prefix='fa') 
    ).add_to(maproute)

    # Destination Marker
    folium.Marker(
        [geocode_dest['lat'], geocode_dest['lng']],
        popup=f"<b>Destination:</b> {destination}",
        icon=folium.Icon(color='darkred', icon='flag', prefix='fa') 
    ).add_to(maproute)
    # ----------------------------------------------


    colors = ["red", "blue", "green"]
    route_details = []

    # 1. Add all alternative routes to the map, showing traffic duration
    for idx, route in enumerate(directions_result):
        leg = route["legs"][0]
        
        distance_text = leg["distance"]["text"]
        
        # *** TRAFFIC INTEGRATION: Use duration_in_traffic if available, otherwise use regular duration ***
        # The Directions API returns 'duration_in_traffic' when 'departure_time' is set.
        duration_in_traffic_data = leg.get('duration_in_traffic', leg['duration'])
        duration_in_traffic_text = duration_in_traffic_data['text']
        duration_in_traffic_value = duration_in_traffic_data['value']
        
        polyline = route["overview_polyline"]["points"]
        decoded_path = decode_polyline(polyline)
        coords = [(point['lat'], point['lng']) for point in decoded_path]

        folium.PolyLine(
            coords,
            color=colors[idx % len(colors)],
            weight=5,
            opacity=0.8,
            # Update the tooltip to clearly state the traffic-aware duration
            tooltip=f"Route {idx+1}: {distance_text}, Traffic Duration: {duration_in_traffic_text}"
        ).add_to(maproute)
        
        route_details.append({
            "route": f"Route {idx+1}",
            "distance_text": distance_text,
            "duration_in_traffic_text": duration_in_traffic_text,
            "duration_in_traffic_value": duration_in_traffic_value,
        })


    # 2. Find and add restaurant markers to the map
    restaurants = find_restaurants_along_route(origin, destination)
    
    for rest in restaurants:
        folium.Marker(
            [rest['location']['lat'], rest['location']['lng']],
            popup=f"<b>{rest['name']}</b><br>Rating: {rest['rating']}<br>{rest['address']}",
            icon=folium.Icon(color='green', icon='cutlery', prefix='fa') 
        ).add_to(maproute)

    map_file = "route_map_with_traffic_and_restaurants.html"
    maproute.save(map_file)
    
    if openmap:
        webbrowser.open(map_file)
        
    return map_file, route_details, restaurants

# ----------------------------------------------------------------------
# Original functions kept for completeness/backward compatibility
# ----------------------------------------------------------------------
# NOTE: The original 'generateroute_with_restaurants' is now replaced by 
# 'generate_route_with_traffic_and_restaurants' for better clarity.

def generate_route(origin, destination, open_map=True):
    """
    Original function to generate route without restaurants or explicit traffic display. 
    It is now set up to call the new comprehensive function.
    """
    print("NOTE: Calling generate_route_with_traffic_and_restaurants to include all features.")
    map_file, route_details, restaurants = generate_route_with_traffic_and_restaurants(origin, destination, open_map)
    
    # Filter details to match the original function's expected return (no restaurant list)
    # The gmaps.directions call is repeated here just to access the full route object 
    # to maintain the minimal_route_details structure used by the Streamlit app.
    full_directions = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now(), alternatives=True)
    
    minimal_route_details = [
        {
            "route": d["route"],
            "distance_text": d["distance_text"],
            "duration_text": d["duration_in_traffic_text"], # Use traffic duration here
            # The 'distance_value' and 'duration_value' need to come from the full directions object
            "distance_value": full_directions[i]["legs"][0]["distance"]["value"],
            "duration_value": d["duration_in_traffic_value"], # Use traffic duration value here
        }
        for i, d in enumerate(route_details)
    ]
    return map_file, minimal_route_details


# --- Only run this if script is executed directly ---
if __name__ == "__main__":
    origin = input("Enter your start location: ")
    destination = input("Enter your destination: ")
    
    # Use the new comprehensive function
    map_file, found_routes, found_restaurants = generate_route_with_traffic_and_restaurants(origin, destination) 

    if map_file:
        print(f"\nMap saved to: {map_file}")
        print("\nFound Routes (Traffic-Aware Duration):")
        for r in found_routes:
            print(f"- {r['route']} | Distance: {r['distance_text']} | Traffic Duration: {r['duration_in_traffic_text']}")
            
        print("\nFound Restaurants:")
        for r in found_restaurants:
            print(f"- {r['name']} (Rating: {r['rating']}, Address: {r['address']})")