from langchain.tools.base import BaseTool
import requests

class HotelSearchTool(BaseTool):
    name = "search_hotels"
    description = "Search for hotels and accommodations using Booking.com API via Rapid API"

    def _run(self, destination_id: str, sort_by: str = "trending", page: int = 1, currency_code: str = "INR", language_code: str = "en-us"):
        url = "https://booking-com15.p.rapidapi.com/api/v1/attraction/searchAttractions"
        querystring = {
            "id": destination_id,
            "sortBy": sort_by,
            "page": str(page),
            "currency_code": currency_code,
            "languagecode": language_code,
        }
        headers = {
            "x-rapidapi-key": "bd9d2138b9msh202b7dca2382ebap1880a6jsn00e24df8fae7",
            "x-rapidapi-host": "booking-com15.p.rapidapi.com",
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise an error for HTTP issues
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("This tool does not support async execution.")
