import math

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from Utilities.EnvironmentVariableLoader import loadEnvVariable
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Literal
from DummyDatas.MockData import MOCK_FLIGHTS
from Tools.UserUpsert import checkAccountBalance, deductUserBalance, checkUserCity
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

MODEL = loadEnvVariable('MINI_MODEL')
FLIGHTPROMPT = """
You are a smart Travel agent responsible for booking flight.
You will look the desire travel date, orgin airport and destination.
You need to look at users budget and any other contrains like number stops, total travel hours, if given.
If not budget is given, check the user's account balance, and make sure user can afford the flight.
If you have flight that meets all criteria book it for user, and perform the financial transaction.
Only if not such flight is available, try to broader the category and come up with suggestion, do not book it.
If there is not such flight available, please respond: NO SUCH FLIGHT AVAILABLE.
"""

llm = ChatOpenAI(model=MODEL)

class FlightDetails(BaseModel):
    id:str  = Field(description='Id of flight')
    airline:str  = Field(description='airline name')
    flight_number:str  = Field(description='flight number')
    departure_city:str  = Field(description='departure city')
    arrival_city:str  = Field(description='Arrival city')
    departure_time:str  = Field(description='departure time')
    arrival_time:str  = Field(description='Arrival time')
    duration:str  = Field(description='duration of flight')
    stops:str  = Field(description='number of stops in trip')
    booking_class:str  = Field(description='Booking class')
    price:str  = Field(description='Price of flight')
    currency:str  = Field(description='Currency of price')


class FlightAgentResponse(BaseModel):
    recommendedFlights: list[FlightDetails] | list = Field(description='Flied for recommended flight recommendations')
    bookFlight:FlightDetails = Field(description='flied for booked flight')
    response:Literal['Booked', 'No flights found'] = Field(description='final response regarding booking')
    originCity:str = Field(description='Field for origin city of flight')
    destinationCity:str = Field(description='Field for city of flight')



@tool('bookFlight')
def bookFlight(flightId:str)->dict:
    """Book the flight with flight id"""
    """
    Args:
        flightId : id of the flight
    Returns:
        detail of the flights
    """
    for city, flights in MOCK_FLIGHTS.items():
        for flight in flights:
            if flight['id'] == flightId:
                return flight
    return {}
    
@tool('flightLookups')
def flightLookups(origin:str, destination:str)->list:
    """Get the flights that goes form origin to destination"""
    """
    Args:
        origin : Origin city of user origin
        destination : destination city
    Returns:
        list of fligths that go form origin to destination
    """
    potentialFlights = []
    if destination in MOCK_FLIGHTS:
        flights = MOCK_FLIGHTS[destination]
        for flight in flights:
            if origin == flight['departure_city']:
                potentialFlights.append(flight)
    return potentialFlights


toolsToUse = [bookFlight, flightLookups,checkAccountBalance, deductUserBalance, checkUserCity]
checkPointer = InMemorySaver()

flightAgent  = create_agent(
    model=MODEL,
    tools=toolsToUse,
    system_prompt=FLIGHTPROMPT,
    middleware=[],
    name= 'FLIGHT_AGENT',
    response_format=FlightAgentResponse,
    checkpointer=checkPointer
)


def main():
    thread_connfig = {"configurable": {"thread_id": "manager_session_456"}}
    try: 
        response = flightAgent.invoke(
            {'messages': [
                HumanMessage(content='my name is Bexter. Book me a flight from my city to Tokyo.')
            ]},
            thread_connfig  
        )
        print(response)
    except Exception as e:
            print(f"Caught Expected Error: {e}\n")
            state_snapshot = flightAgent.get_state(thread_connfig)
            messages = state_snapshot.values.get("messages", [])

if __name__ == "__main__":
    print("This is your Flight Agent!")
    main()
