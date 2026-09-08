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



def scheduleExtraction():
    print(f"============================Activity Agent at Service============================")
    result = scheduleFetchedAgent.invoke({'messages':[ 
        HumanMessage(content="""
            I am traveling for tokyo for 3 days. Please recommend me list of activities to do. 
            My budget is 500 USD.
            Categories I want to cover are Nature, Views and culture.
        """)
    ]})
    print(result['structured_response'])
    return {'ActivityCategoryPerDay' : result['structured_response'].ListOfDesiredActivity}


def main():
    print("Hello from agentic-traveling!")
    scheduleExtraction()

if __name__ == "__main__":
    main()
