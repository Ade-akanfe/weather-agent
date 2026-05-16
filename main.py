import os

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent

from langchain_ollama import ChatOllama
from pprint import pprint
from langchain.tools import tool

load_dotenv()


@tool()
def weather_assistant(city):
    """
       Get weather information, clothing recommendations,
       and activity suggestions for multiple cities.
    """
    weather = check_weather(city)

    if not weather["success"]:
        return weather["error"]

    clothing = clothing_recommendation(weather["temp"])

    activity = activity_recommendation(weather["desc"])

    return f"""
    City: {weather['city']}, {weather['country']}

    Temperature: {weather['temp']}°C
    Condition: {weather['desc']}
    Humidity: {weather['humidity']}%
    Wind Speed: {weather['wind_speed']} m/s

    Clothing Recommendation:
    {clothing}

    Activity Recommendation:
    {activity}
    """


def check_weather(location: str):
    """
       Get the current weather for a location.
    """

    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    # OpenWeatherMap API endpoint
    url = "https://api.openweathermap.org/data/2.5/weather"

    # params
    params = {"q": location, "appid": API_KEY, "units": "metric"}

    # send http response
    response = requests.get(url, params=params, timeout=10)
    # check the response status
    if response.status_code != 200:
        return {
            "success": False,
            "error": f"{response.status_code} at {location} with error {response.text}"
        }

    data = response.json()
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    return {
        "success": True,
        "city": city,
        "country": country,
        "desc": desc,
        "temp": temp,
        "feels_like": feels_like,
        "humidity": humidity,
        "wind_speed": wind_speed
    }


def clothing_recommendation(temp: float):
    """
           Get the clothing recommendation for a location.
        """
    if temp >= 30:
        return "Wear very light clothing and stay hydrated."

    elif temp >= 22:
        return "Light clothing is recommended."

    elif temp >= 15:
        return "A light jacket may be useful."

    elif temp >= 8:
        return "Wear a jacket or sweater."

    else:
        return "Wear warm clothing and a heavy jacket."


def activity_recommendation(description: str):
    """
           Get the activity recommendation for a location.
        """
    description = description.lower()

    if "rain" in description:
        return "Carry an umbrella and avoid outdoor activities."

    if "storm" in description:
        return "Stay indoors if possible."

    if "clear" in description:
        return "Great weather for outdoor activities."

    if "cloud" in description:
        return "Good weather for most activities."

    return "Weather conditions are moderate."

    # define model provider


llm = ChatOllama(model="qwen3:4b")

# create agent
agent = create_agent(
    model=llm,
    tools=[weather_assistant],
    system_prompt="""
You are an intelligent weather assistant.

Provide:
- weather summaries
- clothing recommendations
- activity suggestions
"""
)

for chunk in agent.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in Lagos?"
                }
            ]
        },
        stream_mode="updates"
):

    # Model messages
    if "model" in chunk:

        messages = chunk["model"]["messages"]

        for msg in messages:

            # Tool calls
            if msg.tool_calls:
                print("\n🤖 Agent wants to use tool:\n")

                for tool_call in msg.tool_calls:
                    print(f"Tool: {tool_call['name']}")
                    print(f"Arguments: {tool_call['args']}")

            # Final AI output
            if msg.content:
                print("\n✅ AI Response:\n")
                print(msg.content)

            # Token usage
            if hasattr(msg, "usage_metadata") and msg.usage_metadata:
                print("\n📊 Token Usage:\n")
                pprint(msg.usage_metadata)

    # Tool execution output
    if "tools" in chunk:

        messages = chunk["tools"]["messages"]

        for msg in messages:
            print("\n🛠️ Tool Result:\n")
            print(f"Tool: {msg.name}")
            print(f"Output: {msg.content}")
