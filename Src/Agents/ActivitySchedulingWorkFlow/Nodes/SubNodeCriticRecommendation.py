from langchain.messages import SystemMessage
from Agents.ActivitySchedulingWorkFlow.Agent import recommendationCriticAgent
from Agents.ActivitySchedulingWorkFlow.Schemas import ActivityRecommendationPerDay, DesiredCategoriesForOneDay
from Agents.ActivitySchedulingWorkFlow.Nodes.ScheduleExtraction import scheduleExtraction
from Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeRecommendationGenerator import recommendationGenerator
from Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeRecommendationRegenerator import recommendReGeneratorPerDay
from Agents.ActivitySchedulingWorkFlow.Schemas import SubGraphState
import time

def criticRecommendation(state:SubGraphState):
    # activityRecommendationPerDay:ActivityRecommendationPerDay, desiredCategoriesForOneDay:DesiredCategoriesForOneDay
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

def main():
    # print(f"============================Activity Agent at Service attempt:{attempt}============================")

    # result = scheduleExtraction()
    # activityRecommendationPerDay = recommendActivityPerDay(result['ActivityCategoryPerDay'][0])
    # resultWIthCritics = recommendCriticPerDay(activityRecommendationPerDay['activityRecommendationPerDay'], result['ActivityCategoryPerDay'][0])
    # recommendReGeneratorPerDay(resultWIthCritics['previousSchedule'], resultWIthCritics['critics'])
    pass

if __name__ == "__main__":
    main()
