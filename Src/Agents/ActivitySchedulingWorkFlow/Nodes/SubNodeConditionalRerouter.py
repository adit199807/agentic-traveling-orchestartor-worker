from langchain.messages import HumanMessage
from Agents.ActivitySchedulingWorkFlow.Agent import recommendationGeneraterAgent
from langgraph.graph import END
from Agents.ActivitySchedulingWorkFlow.Schemas import SubGraphState


RECOMMENDATION_CRITIC = 'RECOMMENDATION_CRITIC'

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
