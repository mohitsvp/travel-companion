from crewai import Crew, Agent, Process, Task
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

groq_llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama3-8b-8192",
    temperature=0.0
)

openai_llm = ChatOpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
    temperature=0.0
)

researcher_agent = Agent(
    role = "Researcher",
    goal="Extract the important places to visit in a given city based on user's input i.e. {city}",
    backstory="Developed to automate the process of finding interesting places to visit in a city, this agent utilizes natural language processing (NLP) techniques to identify and categorize key locations.",
    verbose=True,
    llm=openai_llm
)

trip_planner_agent = Agent(
    role = "Trip Planner",
    goal="Provide the itinerary for a trip based on researcher agent's output",
    backstory="Designed to assist in planning trips, this agent leverages natural language processing (NLP) techniques to create iteneraries based on the locations identified by the researcher agent.",
    verbose=True,
    llm=openai_llm
)

researcher_task = Task(
    description="Extract and structure key locations to visit in a city based on user input, using NLP techniques to convert unstructured data into a standardized format.city is {city}",
    expected_output="A structured list of locations to visit in the given city.",
    agent=researcher_agent
)

trip_planner_task = Task(
    description="Create an itinerary for a trip based on the list of locations provided by the researcher agent for the city {city}. The trip duration is {trip_duration}",
    expected_output="A detailed itinerary for the trip, including travel routes, time estimates, and recommended activities.",
    agent=trip_planner_agent,
    context=[researcher_task],
    output_file="trip_itinerary.md"
)

crewai = Crew(
    agents=[researcher_agent, trip_planner_agent],
    tasks=[researcher_task, trip_planner_task],
    verbose=True,
    process = Process.hierarchical,
    manager_llm=openai_llm
)

result = crewai.kickoff({'city' : 'Washington DC', 'trip_duration' : '7 days'})

print(result)