from langchain.messages import SystemMessage
from Agents.ActivitySchedulingWorkFlow.Agent import recommendationReGeneraterAgent
from Agents.ActivitySchedulingWorkFlow.Schemas import TotalDesiredActivities, DesiredCategoriesForOneDay
from Agents.ActivitySchedulingWorkFlow.Nodes.ScheduleExtraction import scheduleExtraction
# from Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeRecommendationGenerator import recommendationGenerator
# from Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeCriticRecommendation import criticRecommendation
from Agents.ActivitySchedulingWorkFlow.Schemas import SubGraphState
import time


def recommendReGeneratorPerDay(state:SubGraphState):
    # desiredCategoriesForOneDay:DesiredCategoriesForOneDay, critics:list[str]
        schedule =  state['activityRecommendationPerDay']
        critics = state['recommendationCriticPerDay'].critics
        result = recommendationReGeneraterAgent.invoke({'messages' : [SystemMessage
                        (content=f""" critics: {critics} and previous schedule: {schedule}
        """)]})

        return {
            'activityRecommendationPerDay' : result['structured_response'],
            'currenTNumberOfIteration' : state['currenTNumberOfIteration']+1
        }

def main():
    # print(f"============================Activity Agent at Service attempt:{attempt}============================")
    result = scheduleExtraction()
    activityRecommendationPerDay = recommendActivityPerDay(result['ActivityCategoryPerDay'][0])
    resultWIthCritics = recommendCriticPerDay(activityRecommendationPerDay['activityRecommendationPerDay'], result['ActivityCategoryPerDay'][0])
    recommendReGeneratorPerDay(resultWIthCritics['previousSchedule'], resultWIthCritics['critics'])

if __name__ == "__main__":
    main()
