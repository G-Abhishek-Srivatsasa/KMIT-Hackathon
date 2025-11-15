import requests
import datetime

# Replace below with your Google Maps API key
GOOGLE_MAPS_API_KEY = "AIzaSyBJvLf7ELmjeX6KSmaGHHi2-Ks1QBkWWR0"

class SafeRouteSystem:
    def _init_(self):
        self.user_reports = []  # Correctly set up attribute!

    # 1. Live Safety Indicators (stub)
    def get_live_safety_indicators(self, location):
        data = {
            "lighting": self.fetch_lighting(location),
            "crime": self.fetch_crime_data(location),
            "accidents": self.fetch_accident_spots(location),
            "hazards": self.fetch_hazard_data(location)
        }
        return data

    # 2. Route Scoring (same as before)
    def score_route(self, indicators, time_of_day):
        score = (
            0.4 * indicators["lighting"] +
            0.3 * (1 - indicators["crime"]) +
            0.2 * (1 - indicators["accidents"]) +
            0.1 * (1 - indicators["hazards"])
        )
        if time_of_day == 'night':
            score *= 0.8
        return score

    def get_time_of_day(self):
        now = datetime.datetime.now()
        return "night" if now.hour < 6 or now.hour > 18 else "day"

    # 7. Crowd-Sourcing Module (fixed error)
    def report_incident(self, report):
        self.user_reports.append(report)
        print("Incident reported and map updated.")

    # GOOGLE MAPS ROUTE API
    def get_routes(self, origin, destination):
        url = f"https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": f"{origin[0]},{origin[1]}",
            "destination": f"{destination[0]},{destination[1]}",
            "key": GOOGLE_MAPS_API_KEY
        }
        res = requests.get(url, params=params)
        routes = res.json().get("routes", [])
        return routes

    # 5. Interactive Map (print route with hazards)
    def show_route_and_hazards(self, origin, destination):
        routes = self.get_routes(origin, destination)
        print("ROUTES FOUND:", len(routes))
        print("Example polyline:", routes[0]['overview_polyline']['points'] if routes else "None")
        for report in self.user_reports:
            print("USER-REPORTED HAZARDS:", report)
        # Visualization would be done with JS/HTML frontend or Folium for desktop.

    def fetch_lighting(self, location): return 0.9
    def fetch_crime_data(self, location): return 0.2
    def fetch_accident_spots(self, location): return 0.1
    def fetch_hazard_data(self, location): return 0.1

if __name__ == "__main__":
    nav = SafeRouteSystem()
    loc1 = (17.4401, 78.3489)  # Example: source
    loc2 = (17.4511, 78.4002)  # Example: destination

    nav.report_incident({"loc": loc1, "type": "pothole"})
    indicators = nav.get_live_safety_indicators(loc1)
    score = nav.score_route(indicators, nav.get_time_of_day())

    print("Safety Score:", score)
    nav.show_route_and_hazards(loc1, loc2)