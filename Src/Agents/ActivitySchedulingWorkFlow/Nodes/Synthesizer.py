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
from ActivitySchedulingWorkFlow.Schemas import GraphState

def synthersizer(state:GraphState):
    state['activityAgentResponse'].listOfActivityPerDay.append(state['activityRecommendationPerDay'])
    return {'activityAgentResponse' : state['activityAgentResponse']}

