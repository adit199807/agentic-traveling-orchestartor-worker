from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from Utilities.EnvironmentVariableLoader import loadEnvVariable
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Literal
from DummyDatas.MockData import MOCK_ACTIVITIES
from Tools.UserUpsert import checkAccountBalance, deductUserBalance, checkUserCity
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph


MODEL = loadEnvVariable('MINI_MODEL')

@tool('activityLookUp')
def activityLookUp(destinationCity:str, category:str)->list:
    """Lookup for acitvities the given category"""
    """
    Args:
        destinationCity : City to lookup activity for
        category: categories of activity to lookup for
    Returns:
        List of activities in the ciy that are covered in the category 
    """
    filteredActivity = []
    for city, activities in MOCK_ACTIVITIES.items():
            if city.lower() != destinationCity.lower():
                continue 
            for activity in activities:
                if activity['category'] == category:
                    filteredActivity.append(activity)
    return filteredActivity

availLableTools = [activityLookUp]
llm = ChatOpenAI(model=MODEL)

scheduleFetchedAgent = create_agent(llm,
                            system_prompt=ACTIVITY_CATEGORY_FETCHER,
                            response_format=TotalDesiredActivities
                        )
activityAgent = create_agent(llm,
                            system_prompt=ACTIVITY_AGENT_PROMPT,
                            tools=availLableTools,
                            response_format=ActivityAgentResponse
                        )
criticActivityAgent = create_agent(llm,
                            system_prompt=ACTIVITY_AGENT_PROMPT,
                            tools=availLableTools,
                            response_format=ActivityAgentResponse
                        )



def main():
    attempt = 3
    while attempt:
        try:
            print(f"============================Activity Agent at Service attempt:{attempt}============================")
            result = activityAgent.invoke({'messages':[
                HumanMessage(content="""
                I am traveling for tokyo for 3 days. Please recommend me list of activities to do. 
                My budget is 500 USD.
                Categories I want to cover are Nature, Views and culture.
                """)]})
            print(result)
        except Exception as e:
            print(e)
            attempt-=1

if __name__ == "__main__":
    main()
