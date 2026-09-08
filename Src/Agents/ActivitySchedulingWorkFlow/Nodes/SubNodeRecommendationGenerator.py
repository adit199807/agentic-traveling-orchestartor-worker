from langchain.messages import HumanMessage
from Agents.ActivitySchedulingWorkFlow.Agent import recommendationGeneraterAgent
from ActivitySchedulingWorkFlow.Schemas import SubGraphState


def recommendationGenerator(state:SubGraphState):
    userPref =  state['desiredCategoriesForOneDay']
    city = userPref.city
    categories = userPref.category
    budget = userPref.budgetPerDay

    result = recommendationGeneraterAgent.invoke({'messages' : [HumanMessage
                    (content=f""" the desired city is: {city} and following categories: {categories}
                    with total budget : {budget}
            """)]})
    return {'activityRecommendationPerDay' : result['structured_response']}


def main():
    # print(f"============================Activity Agent at Service attempt:{attempt}============================")

    # result = scheduleExtraction()
    # recommendActivityPerDay(result['ActivityCategoryPerDay'])
    pass

if __name__ == "__main__":
    main()
