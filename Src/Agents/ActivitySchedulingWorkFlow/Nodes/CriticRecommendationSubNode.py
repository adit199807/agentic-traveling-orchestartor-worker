from langchain.messages import SystemMessage
from Agents.ActivitySchedulingWorkFlow.Agent import recommendationCriticAgent
from Agents.ActivitySchedulingWorkFlow.Schemas import ActivityRecommendationPerDay, DesiredCategoriesForOneDay
from Agents.ActivitySchedulingWorkFlow.Nodes.ScheduleExtraction import scheduleExtraction
from Agents.ActivitySchedulingWorkFlow.Nodes.ActivityRecommenderSubNode import recommendActivityPerDay
from Agents.ActivitySchedulingWorkFlow.Nodes.RecommendationRegenerator import recommendReGeneratorPerDay

import time

def recommendCriticPerDay(activityRecommendationPerDay:ActivityRecommendationPerDay, desiredCategoriesForOneDay:DesiredCategoriesForOneDay):
    attempt = 0
    while attempt<4:
        try:
            schedule = activityRecommendationPerDay.recommendedActivitySchedule
            userPref =  desiredCategoriesForOneDay
            city = userPref['city']
            categories = userPref['category']
            budget = userPref['budgetPerDay']
            result = recommendationCriticAgent.invoke({'messages' : [SystemMessage
                            (content=f"""
                            User prefrenced city:{city}, categories:{categories} and budget:{budget}
                            Following schedule:
                            {schedule} 
        """)]})
            return {'critics': result['structured_response'].critics, 'previousSchedule' :schedule }
        except Exception as e:
                    print(e)
                    attempt += 1
                    time.sleep(60)

        return {'critics': [], 'previousSchedule' :schedule }
        

def main():
    # print(f"============================Activity Agent at Service attempt:{attempt}============================")

    result = scheduleExtraction()
    activityRecommendationPerDay = recommendActivityPerDay(result['ActivityCategoryPerDay'][0])
    resultWIthCritics = recommendCriticPerDay(activityRecommendationPerDay['activityRecommendationPerDay'], result['ActivityCategoryPerDay'][0])
    recommendReGeneratorPerDay(resultWIthCritics['previousSchedule'], resultWIthCritics['critics'])

if __name__ == "__main__":
    main()
