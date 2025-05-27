import math
import httpx

async def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth specified in decimal degrees.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Radius of Earth in kilometers (use 3956 for miles)
    r = 6371.0
    return c * r


async def geocode_address(address: str) -> dict:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "ConnectWithTutor/1.0 (contact@bachminhtuyen.id.vn)"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        results = response.json()

        if not results:
            raise ValueError("Address not found")

        location = results[0]
        return {
            "latitude": float(location["lat"]),
            "longitude": float(location["lon"]),
            "display_name": location["display_name"]
        }

async def get_coordinates_from_details(osm_type: str, osm_id: int) -> dict:
    osm_type_map = {"node": "N", "way": "W", "relation": "R"}
    osm_short_type = osm_type_map.get(osm_type.lower())
    if not osm_short_type:
        raise ValueError("Invalid OSM type")

    url = "https://nominatim.openstreetmap.org/details.php"
    params = {
        "osmtype": osm_short_type,
        "osmid": osm_id,
        "format": "json"
    }

    headers = {
        "User-Agent": "ConnectWithTutor/1.0 (contact@bachminhtuyen.id.vn)"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Ensure centroid exists
        if "centroid" not in data or "coordinates" not in data["centroid"]:
            raise ValueError("No coordinates found in details")

        lng, lat = data["centroid"]["coordinates"]
        return {
            "lat": float(lat),
            "lng": float(lng),
            "display_name": data.get("localname", "")
        }


async def get_location_details(address: str):
    search_url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "ConnectWithTutor/1.0 (contact@bachminhtuyen.id.vn)"}
    async with httpx.AsyncClient() as client:
        search_response = await client.get(
            search_url, 
            params={"q": address, "format": "json", "limit": 1}, 
            headers=headers
        )
        search_response.raise_for_status()
        search_data = search_response.json()

        if not search_data:
            raise ValueError("Address not found")

        result = search_data[0]
        osm_id = result["osm_id"]
        osm_type = result["osm_type"]

        # Get lat/lon from details
        location = await get_coordinates_from_details(osm_type, osm_id)

        return {
            "latitude": location["lat"],
            "longitude": location["lng"],
            "display_name": location["display_name"]
        }
