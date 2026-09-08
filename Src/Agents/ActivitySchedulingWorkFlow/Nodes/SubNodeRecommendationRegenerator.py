from langchain.messages import SystemMessage
from Agents.ActivitySchedulingWorkFlow.Agent import recommendationReGeneraterAgent
from Agents.ActivitySchedulingWorkFlow.Schemas import TotalDesiredActivities, DesiredCategoriesForOneDay
from Agents.ActivitySchedulingWorkFlow.Nodes.ScheduleExtraction import scheduleExtraction
from Src.Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeActivityRecommender import recommendActivityPerDay
from Src.Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeCriticRecommendation import recommendCriticPerDay
from ActivitySchedulingWorkFlow.Schemas import SubGraphState
import time


def recommendReGeneratorPerDay(state:SubGraphState):
    # desiredCategoriesForOneDay:DesiredCategoriesForOneDay, critics:list[str]
    attempt = 0
    while attempt<4:
        try:
            schedule =  state['activityRecommendationPerDay']
            critics = state['recommendationCriticPerDay'].critics
            result = recommendationReGeneraterAgent.invoke({'messages' : [SystemMessage
                            (content=f""" critics: {critics} and previous schedule: {schedule}
            """)]})

            return {
                'activityRecommendationPerDay' : result['structured_response'],
                'currenTNumberOfIteration' : state['currenTNumberOfIteration']+1
            }
        except Exception as e:
            print(e)
            attempt += 1
            time.sleep(60)
            
            return{
                    'activityRecommendationPerDay' : state['activityRecommendationPerDay'],
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
