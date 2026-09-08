from pydantic import BaseModel, Field
from typing import Literal
from typing import TypedDict, Annotated

class DesiredCategoriesForOneDay(BaseModel):
    """Use this structure for city user is going to be for one day, and category they want to cover in one day"""
    city:str = Field(description='City your is going to be for one day')
    category: list[str] = Field(description='Categories of acitivty to be covered for one day')
    budgetPerDay: list[str] = Field(description='Budget available for one day')


class TotalDesiredActivities(BaseModel):
    ListOfDesiredActivity:list[DesiredCategoriesForOneDay] | list = Field(description=""" List of desired category in the required city.' \
    Each element signifies one day.""")



class ActivityDetails(BaseModel):
    id: str = Field(description='Id of activity')
    name: str = Field(description='Name of activity')
    category: str = Field(description='Category of activity')
    duration: str = Field(description='Duration of activity')
    price: str = Field(description='Price of activity')
    currency: str = Field(description='Currency of activity')
    rating: str = Field(description='Rating of activity')
    description: str = Field(description='Description of activity')
    best_for: str = Field(description='Best for activity')
    location: str = Field(description='location of activity')


class ActivityRecommendationPerDay(BaseModel):
    recommendedActivitySchedule: list[ActivityDetails] | list = Field(description='Flied to store schedule of activities.')

class RecommendationCriticPerDay(BaseModel):
    critics: list[str] | list = Field(description='List of critics to improve the recommendation.')


class ActivityAgentResponse(BaseModel):
    listOfActivityPerDay: list[ActivityRecommendationPerDay] | list = Field(description='List of list of activity recommended per day.')

class GraphState(TypedDict):
    userInput : str| None
    totalDesiredActivities : TotalDesiredActivities | None
    activityAgentResponse :  ActivityAgentResponse| None
    activityRecommendationPerDay :  ActivityRecommendationPerDay| None

class SubGraphState(TypedDict):
    desiredCategoriesForOneDay : DesiredCategoriesForOneDay| None
    activityRecommendationPerDay : ActivityRecommendationPerDay| None
    recommendationCriticPerDay : RecommendationCriticPerDay| None
    currenTNumberOfIteration : int| None
