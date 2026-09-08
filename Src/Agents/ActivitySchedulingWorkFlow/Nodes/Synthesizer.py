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


class ActivityRecommendedForTrip(BaseModel):
    listOfActivityPerDay: list[ActivityPerDay] | list = Field(description='List of list of activity recommended per day.')
