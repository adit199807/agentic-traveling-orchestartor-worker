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
from Agents.ActivitySchedulingWorkFlow.Agent import recommendationGeneraterAgent
from Agents.ActivitySchedulingWorkFlow.Tools import activityLookUp
from Agents.ActivitySchedulingWorkFlow.Schemas import TotalDesiredActivities, DesiredCategoriesForOneDay
from Agents.ActivitySchedulingWorkFlow.Nodes.ScheduleExtraction import scheduleExtraction


def recommendActivityPerDay(desiredCategoriesForOneDay:DesiredCategoriesForOneDay):
    lis = []
    schedule =  desiredCategoriesForOneDay
    city = schedule['city']
    categories = schedule['category']
    budget = schedule['budgetPerDay']
    result = recommendationGeneraterAgent.invoke({'messages' : [HumanMessage
                    (content=f""" the desired city is: {city} and following categories: {categories}
                    with total budget : {budget}
""")]})
    return {'activityRecommendationPerDay' : result['structured_response']}


def main():
    # print(f"============================Activity Agent at Service attempt:{attempt}============================")

    result = scheduleExtraction()
    recommendActivityPerDay(result['ActivityCategoryPerDay'])
    # attempt = 3
    # while attempt:
    #     try:
    #         result = activityRecommenderAgent.invoke({'messages':[
    #             HumanMessage(content="""
    #             I am traveling for tokyo for 3 days. Please recommend me list of activities to do. 
    #             My budget is 500 USD.
    #             Categories I want to cover are Nature, Views and culture.
    #             """)]})
    #         print(result)
    #     except Exception as e:
    #         print(e)
    #         attempt-=1

if __name__ == "__main__":
    main()
