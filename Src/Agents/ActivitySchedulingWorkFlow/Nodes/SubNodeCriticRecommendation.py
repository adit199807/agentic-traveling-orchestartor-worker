from langchain.messages import SystemMessage
from Agents.ActivitySchedulingWorkFlow.Agent import recommendationCriticAgent
from Agents.ActivitySchedulingWorkFlow.Schemas import ActivityRecommendationPerDay, DesiredCategoriesForOneDay
from Agents.ActivitySchedulingWorkFlow.Nodes.ScheduleExtraction import scheduleExtraction
from Src.Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeRecommendationGenerator import recommendationGenerator
from Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeRecommendationRegenerator import recommendReGeneratorPerDay
from ActivitySchedulingWorkFlow.Schemas import SubGraphState


import time

def criticRecommendation(state:SubGraphState):
    # activityRecommendationPerDay:ActivityRecommendationPerDay, desiredCategoriesForOneDay:DesiredCategoriesForOneDay
    attempt = 0
    while attempt<4:
        try:
            schedule = state['activityRecommendationPerDay'].recommendedActivitySchedule
            userPref =  state['desiredCategoriesForOneDay']
            city = userPref.city
            categories = userPref.category
            budget = userPref.budgetPerDay
            result = recommendationCriticAgent.invoke({'messages' : [SystemMessage
                            (content=f"""
                            User prefrenced city:{city}, categories:{categories} and budget:{budget}
                            Following schedule:
                            {schedule} 
            """)]})
            return {'recommendationCriticPerDay': result['structured_response']}
        except Exception as e:
                    print(e)
                    attempt += 1
                    time.sleep(60)

        return {'critics': [], 'previousSchedule' :schedule }
        

def main():
    # print(f"============================Activity Agent at Service attempt:{attempt}============================")

    # result = scheduleExtraction()
    # activityRecommendationPerDay = recommendActivityPerDay(result['ActivityCategoryPerDay'][0])
    # resultWIthCritics = recommendCriticPerDay(activityRecommendationPerDay['activityRecommendationPerDay'], result['ActivityCategoryPerDay'][0])
    # recommendReGeneratorPerDay(resultWIthCritics['previousSchedule'], resultWIthCritics['critics'])
    pass

if __name__ == "__main__":
    main()
