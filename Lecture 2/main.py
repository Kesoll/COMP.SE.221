from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

def get_weather_data(city: str, api_key: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching weather data")

# Load API key from environment variable (you can set it locally for testing)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

app = FastAPI()

# Input model for API request
class City(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather API! Use the /weather endpoint to fetch data."}

@app.post("/weather/")
def fetch_weather(city: City):
    if API_KEY == "your_api_key_here":
        raise HTTPException(status_code=500, detail="API key is not set. Please configure it.")

    weather_data = get_weather_data(city.name, API_KEY)
    return {
        "city": weather_data.get("name"),
        "temperature": weather_data["main"].get("temp"),
        "description": weather_data["weather"][0].get("description"),
        "country": weather_data["sys"].get("country"),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
