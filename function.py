from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import json
import requests

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

tools = [
  {
      "type": "function",
      "function": {
          "name": "get_location",
          "parameters": {
              "type": "object",
              "properties": {
                    "location": {"type": "string", "description" : "city to visit"},
              },
          },
          "required" : ["location"],
      },
  }
]


st.title("Trip Planner")

query = st.text_input("Where are you planning to go?")

if query:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
        tools=tools,
    )

    if completion.choices[0].message.tool_calls:

        location = json.loads(completion.choices[0].message.tool_calls[0].function.arguments)


        location = location["location"]

        if location:

            results = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid=d2fd177875acbf85a3aeee4dcce4319b")

            if results:

                completion2 = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": "Identify the city weather conditions from the data given by the user and provide a list of clothing items that would be suitable for the weather conditions and the things user should pack before heading on to the journey."
                        },
                        {
                            "role" : "user",
                            "content" : str(results.json())
                        }
                    ],
                )



                if completion2.choices[0].message.content:
                    completion3 = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": f"User wants to go to {location} and there is list of travel packing details provided by the user. Can you create an itenary based on the location, 7 days trip clothing requirements, weather details and the user's travel packing details?"
                        },
                        {
                            "role" : "user",
                            "content" : f"weather details : {str(results.json())}"
                        },
                        {
                            "role" : "user",
                            "content" : "clothing details" + completion2.choices[0].message.content
                        }
                    ],
                )
                    

                if completion3.choices[0].message.content:    
                    st.write(completion3.choices[0].message.content)

            
            
    else:
        st.write("I am not sure where you want to go")















# api.openweathermap.org/data/2.5/forecast?q={city name}&appid=d2fd177875acbf85a3aeee4dcce4319b