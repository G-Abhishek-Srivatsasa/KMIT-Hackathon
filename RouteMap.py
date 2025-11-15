import googlemaps
import folium
import webbrowser
from datetime import datetime
from googlemaps.convert import decode_polyline



API_KEY = "AIzaSyBJvLf7ELmjeX6KSmaGHHi2-Ks1QBkWWR0"
gmaps = googlemaps.Client(key=API_KEY)

def generate_route(origin, destination, open_map=True):
    import googlemaps, folium, webbrowser

    gmaps = googlemaps.Client(key=API_KEY)

    directions_result = gmaps.directions(
        origin,
        destination,
        mode="driving",
        departure_time=datetime.now(),
        alternatives=True
    )

    if not directions_result:
        return None, []

    # Create a map centered between origin & destination
    geocode_origin = gmaps.geocode(origin)[0]['geometry']['location']
    geocode_dest = gmaps.geocode(destination)[0]['geometry']['location']
    mid_lat = (geocode_origin['lat'] + geocode_dest['lat']) / 2
    mid_lng = (geocode_origin['lng'] + geocode_dest['lng']) / 2

    map_route = folium.Map(location=[mid_lat, mid_lng], zoom_start=13)

    colors = ["red", "blue", "green"]
    route_details = []

    for idx, route in enumerate(directions_result):
        leg = route["legs"][0]
        distance_text = leg["distance"]["text"]
        duration_text = leg["duration"]["text"]
        distance_value = leg["distance"]["value"]
        duration_value = leg["duration"]["value"]

        polyline = route["overview_polyline"]["points"]
        decoded_path = decode_polyline(polyline)

        coords = [(point['lat'], point['lng']) for point in decoded_path]

        folium.PolyLine(
            coords,
            color=colors[idx % len(colors)],
            weight=5,
            opacity=0.8,
            tooltip=f"Route {idx+1}: {distance_text}, {duration_text}"
        ).add_to(map_route)

        route_details.append({
            "route": f"Route {idx+1}",
            "distance_text": distance_text,
            "duration_text": duration_text,
            "distance_value": distance_value,
            "duration_value": duration_value,
        })

    map_file = "route_map.html"
    map_route.save(map_file)

    if open_map:
        webbrowser.open(map_file)

    return map_file, route_details



# --- Only run this if script is executed directly ---
if __name__ == "__main__":
    origin = input("Enter your start location: ")
    destination = input("Enter your destination: ")
    generate_route(origin, destination)
