from crewai import Agent
from textwrap import dedent
from tools.search_tools import SearchTools
from tools.calculator_tools import CalculatorTools
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Create the model
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     verbose=True,
#     temperature=0.0,
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    verbose=True,
    generation_config=generation_config,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)


class TravelAgent:
    def expert_travel_agent(self):
        return Agent(
            role="Expert Travel Agent",
            backstory=dedent(
                f"""
                             An experienced travel planner specializing in creating efficient and enjoyable itineraries for travelers of all types.
                             """
            ),
            goal=dedent(
                f"""
                        Design comprehensive travel itineraries with per-day plans, budget estimates, packing suggestions, and safety tips.
                        """
            ),
            tools=[
                SearchTools.search_internet,
                CalculatorTools.calculate,
            ],
            verbose=True,
            llm=llm,
        )

    def city_selection_expert(self):
        return Agent(
            role="City Selection Expert",
            backstory=dedent(
                f"""
                             Expert at analyzing travel data to pick ideal destinations
                             """
            ),
            goal=dedent(
                f"""
                        Select the best cities based on weather, season, prices, and traveler interests
                        """
            ),
            tools=[
                SearchTools.search_internet,
            ],
            verbose=True,
            llm=llm,
        )

    def local_tour_guide(self):
        return Agent(
            role="Local Tour Guide",
            backstory=dedent(
                f"""
                             A local expert providing rich insights into the city's attractions, culture, and customs.
                             """
            ),
            goal=dedent(
                f"""
                        Offer in-depth, practical advice about the selected city to maximize the traveler's experience.
                        """
            ),
            tools=[
                SearchTools.search_internet,
            ],
            verbose=True,
            llm=llm,
        )
