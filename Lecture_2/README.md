# COMP.SE.221

## Lecture 2

## Weather Microservice

This microservice provides real-time weather data for a given city using the OpenWeatherMap API. It is built with FastAPI for high performance and easy deployment.

## Features

Fetches current weather details including temperature, description, and country.

Uses FastAPI for quick API responses and automatic documentation.

Simple JSON-based request and response structure.

## Installation

Clone the repository:

git clone <repo-url>
cd weather-microservice

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

### Install dependencies:

pip install -r requirements.txt

## Usage

Set your OpenWeatherMap API key as an environment variable: 

Additionally the API key can be put locally as hardcoded in the code.

export OPENWEATHER_API_KEY="your_api_key_here"

Run the microservice:

uvicorn main:app --reload

Access the API documentation at:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

### API Endpoint

POST /weather/

### Request JSON:

{ "name": "London" }

### Response JSON:

{
  "city": "London",
  "temperature": 8.5,
  "description": "clear sky",
  "country": "GB"
}

### License

This project is open-source and available under the MIT License.

 