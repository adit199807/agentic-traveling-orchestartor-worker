from Agents.ActivitySchedulingWorkFlow.Prompts import (
    ACTIVITY_CATEGORY_FETCHER, 
    ACTIVITY_RECOMMMENDER_AGENT_PROMPT, 
    Critic_ACTIVITY_AGENT_PROMPT,
    ACTIVITY_RECOMMMENDER_WITH_CRITICS_AGENT_PROMPT
    )
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from Utilities.EnvironmentVariableLoader import loadEnvVariable
from Agents.ActivitySchedulingWorkFlow.Schemas import (
    ActivityAgentResponse, 
    ActivityDetails, 
    ActivityRecommendationPerDay, 
    DesiredCategoriesForOneDay, 
    TotalDesiredActivities, 
    RecommendationCriticPerDay
 )
from Agents.ActivitySchedulingWorkFlow.Tools import activityLookUp

MODEL = loadEnvVariable('MINI_MODEL')
llm = ChatOpenAI(model=MODEL)

scheduleFetchedAgent = create_agent(llm,
                            system_prompt=ACTIVITY_CATEGORY_FETCHER,
                            response_format=TotalDesiredActivities
                        )

recommendationGeneraterAgent = create_agent(llm,
                            system_prompt=ACTIVITY_RECOMMMENDER_AGENT_PROMPT,
                            tools=[activityLookUp],
                            response_format=ActivityRecommendationPerDay
                        )

recommendationCriticAgent = create_agent(llm,
                            system_prompt=Critic_ACTIVITY_AGENT_PROMPT,
                            tools=[activityLookUp],
                            response_format=RecommendationCriticPerDay
                        )

recommendationReGeneraterAgent = create_agent(llm,
                            system_prompt=ACTIVITY_RECOMMMENDER_WITH_CRITICS_AGENT_PROMPT,
                            tools=[activityLookUp],
                            response_format=ActivityRecommendationPerDay
                        )