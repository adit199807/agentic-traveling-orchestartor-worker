from langchain.messages import HumanMessage
from Agents.ActivitySchedulingWorkFlow.Agent import recommendationGeneraterAgent
from langgraph.graph import END
from ActivitySchedulingWorkFlow.Schemas import SubGraphState
from ActivitySchedulingWorkFlow.Graph.SubGraph import RECOMMENDATION_CRITIC 

def conditionalRerouter(state:SubGraphState):
    if state['currenTNumberOfIteration'] < 3:
        return RECOMMENDATION_CRITIC
    return END

def main():
    # print(f"============================Activity Agent at Service attempt:{attempt}============================")

    # result = scheduleExtraction()
    # recommendActivityPerDay(result['ActivityCategoryPerDay'])
    pass

if __name__ == "__main__":
    main()
