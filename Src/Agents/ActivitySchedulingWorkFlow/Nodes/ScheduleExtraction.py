from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from Utilities.EnvironmentVariableLoader import loadEnvVariable
from langchain.tools import tool
from DummyDatas.MockData import MOCK_ACTIVITIES
from Tools.UserUpsert import checkAccountBalance, deductUserBalance, checkUserCity
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from Agents.ActivitySchedulingWorkFlow.Agent import scheduleFetchedAgent
from Agents.ActivitySchedulingWorkFlow.Schemas import GraphState



def scheduleExtraction(state:GraphState):
    print(f"============================Activity Agent at Service============================")
    result = scheduleFetchedAgent.invoke({'messages':[HumanMessage(content=f"""{state['userInput']}""")]})
    return {'totalDesiredActivities' : result['structured_response']}


def main():
    print("Hello from agentic-traveling!")
    # scheduleExtraction()

if __name__ == "__main__":
    main()
