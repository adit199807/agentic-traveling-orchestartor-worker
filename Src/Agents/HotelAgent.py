from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from Utilities.EnvironmentVariableLoader import loadEnvVariable
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Literal
from DummyDatas.MockData import MOCK_HOTELS
from Tools.UserUpsert import checkAccountBalance, deductUserBalance, checkUserCity
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

MODEL = loadEnvVariable('MINI_MODEL')
HOTEL_AGENT_PROMPT = """
You are a smart Hotel agency responsible for booking Hotel with lowest cost possible meeting user's criteria.
You will look at desire travel destination and book Hotel room for slected dates accordingly.
Most of the Hotel data does not have dates mentioned, means they are pretty much available for all dates.
You need to look at users budget and any other contrains.
If not budget is given, check at the available blance in user's account, and make sure user can afford the hotel.
If you have hotel that meets all criteria book it for user, and perform the financial transaction.
Only if not such hotel is available, try to broaden the category and come up with suggestion, do not book it.
If there is not such hotels available, please respond: NO SUCH FLIGHT AVAILABLE.
"""


llm = ChatOpenAI(model=MODEL)

class HotelDetails(BaseModel):
    id:str  = Field(description='Id of Hotel')
    hotel_name:str  = Field(description='Hotel name')
    city:str  = Field(description='location city of the hotel')
    dates:list[str]  = Field(description='List of dates for which hotel has been booked for')
    price:str  = Field(description='Total cost of reservation')


class HotelAgentResponse(BaseModel):
    recommendedHotels: list[HotelDetails] | list = Field(description='Flied for recommended hotel recommendations')
    bookHotel:HotelDetails | None = Field(description='flied for booked hotel')
    response:Literal['Booked', 'No Hotel found'] = Field(description='final response regarding booking')



@tool('bookHotel')
def bookHotel(hotelId:str, dates:list[str])->dict:
    """Book the hotel with hotel id for the given dates"""
    """
    Args:
        hotelId : id of the hotel
        dates : list of dates for which hotel is needed for
    Returns:
        detail of the book hotel
    """
    for city, hotels in MOCK_HOTELS.items():
            for hotel in hotels:
                if hotel['id'] == hotelId:
                    if 'dates' not in hotel:
                        return hotel
    return {}

@tool('hotelLookUp')
def hotelLookUp(destinationCity:str, dates:list[str])->dict:
    """Look up hotels the given dates for given location and dates"""
    """
    Args:
        destinationCity : city where hotel is to be booked
        dates : list of dates for which hotel is needed for
    Returns:
        detail of the book hotel
    """
    hotelList = []
    for city, hotels in MOCK_HOTELS.items():
        if city == destinationCity:
            for hotel in hotels:
                if hotel['id'] == hotel:
                    hotelList.append(hotel)
    return hotelList


toolsToUse = [bookHotel, hotelLookUp,checkAccountBalance, deductUserBalance, checkUserCity]
checkPointer = InMemorySaver()
hotelAgent = create_agent(
    model=MODEL,
    system_prompt=HOTEL_AGENT_PROMPT,
    tools=toolsToUse, 
    checkpointer=checkPointer, 
    name='HOTEL_AGENT',
    response_format=HotelAgentResponse
)


def main():
    print("============================Hotel Agent at Service============================")
    thread_connfig = {"configurable": {"thread_id": "manager_session_456"}}
    try:
        response = hotelAgent.invoke(
            {'messages' : 
                           [HumanMessage(content='My name is Dexter. Book me a hotel for 09/18/2026 to 09/20/2026, in tokyo. My budget is 50 dollas')]
            },  
            thread_connfig
        )
        print(response)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
