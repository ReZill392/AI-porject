from crewai import Task
from textwrap import dedent

class TravelTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def plan_itinerary(self, agent, city, range, interests, pricing_tiers, hotelQuality, foodIncluded):
        return Task(
            description=dedent(
                f"""
                **Task**: Develop a {range} Travel Itinerary

                **Description**: Expand the city guide into a full {range} travel itinerary with:
                - Detailed per-day plans, including weather forecasts and recommended activities.
                - **Specific places to eat and stay**, tailored to the traveler's budget ({pricing_tiers}) and preferences.
                - Packing suggestions, ensuring travelers are prepared for the destination and season.
                - A **comprehensive budget breakdown**:
                    - Transportation: (e.g., flights, local transit, taxis)
                    - Accommodation: (e.g., hotel costs per night)
                    - Meals: (e.g., average daily expenses)
                    - Activities: (e.g., entrance fees, optional tours).

                The itinerary should cover all aspects of the trip, from arrival to departure, combining city guide insights with practical travel logistics. Include a total cost summary for all expenses.

                **Parameters**:
                - City: {city}
                - Trip Date: {range}
                - Traveler Interests: {interests}
                - Pricing_tiers: {pricing_tiers}
                - Hotelquality: {hotelQuality}
                - FoodIncluded: {foodIncluded}

                **Note**: {self.__tip_section()} 
                """
            ),
            agent=agent,
            expected_output="A detailed travel itinerary with per-day plans, budget summary, and practical tips.",
        )

    def identify_city(self, agent, origin, cities, interests, range):
        return Task(
            description=dedent(
                f"""
                **Task**: Identify the Best City for the Trip
                **Description**: Analyze and select the best city for the trip based on specific criteria such as weather patterns, seasonal events, and travel costs. 
                This task involves comparing multiple cities, considering factors like current weather conditions, upcoming cultural or seasonal events, and overall travel expenses. 
                Your final answer must be a detailed report on the chosen city, including actual flight costs, weather forecast, and attractions.
                    
                **Parameters**:
                - Origin: {origin}
                - City: {cities}
                - Interests: {interests}
                - Travel Date: {range}
                
                **Note**: {self.__tip_section()} 
                """
            ),
            agent=agent,
            expected_output="",
        )
        
    def gather_city_info(self, agent, city, range, interests, hotelquality, foodincluded):
        return Task(
            description=dedent(
                f"""
                **Task**: Gather In-depth City Guide Information
                **Description**: Compile an in-depth guide for the selected city, gathering information about key attractions, local customs, special events, and daily activity recommendations. 
                This guide should provide a thorough overview of what the city has to offer, including hidden gems, cultural hotspots, must-visit landmarks, weather forecasts, and high-level cost
                    
                **Parameters**:
                - Cities: {city}
                - Interests: {interests}
                - Travel Date: {range}
                - Loccal Food: {foodincluded}
                - Hotelquality: {hotelquality}
                
                **Note**: {self.__tip_section()} 
                """
            ),
            agent=agent,
            expected_output="",
        )
