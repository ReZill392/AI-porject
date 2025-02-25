from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    provider="google-gen-ai",
    callbacks=None  # ปิด callback
)

try:
    response = llm.invoke("Create a travel itinerary for 3 days in Singapore.")
    print(response)
except Exception as e:
    print(f"Error: {e}")
