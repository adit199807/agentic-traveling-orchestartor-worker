from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import RetryPolicy

from Agents.ActivitySchedulingWorkFlow.Schemas import SubGraphState
from Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeRecommendationGenerator import recommendationGenerator
from Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeCriticRecommendation import criticRecommendation
from Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeRecommendationRegenerator import recommendReGeneratorPerDay
from Agents.ActivitySchedulingWorkFlow.Nodes.SubNodeConditionalRerouter import conditionalRerouter
from Agents.ActivitySchedulingWorkFlow.Schemas import GraphState, DesiredCategoriesForOneDay


RECOMMENDATION_GENERATOR = 'RECOMMENDATION_GENERATOR'
RECOMMENDATION_CRITIC = 'RECOMMENDATION_CRITIC'
RECOMMENDATION_REGENERATOR = 'RECOMMENDATION_REGENERATOR'
RECOMMENDATION_CONDITIONAL_ROUTING = 'RECOMMENDATION_CONDITIONAL_ROUTING'

graphFlow = StateGraph(SubGraphState)
graphFlow.add_node(RECOMMENDATION_GENERATOR, 
                   recommendationGenerator,
                retry_policy=RetryPolicy(initial_interval = 30, backoff_factor=3, max_attempts=3))
graphFlow.add_node(RECOMMENDATION_CRITIC, 
                   criticRecommendation,
                   retry_policy=RetryPolicy(initial_interval = 30, backoff_factor=3, max_attempts=3))
graphFlow.add_node(RECOMMENDATION_REGENERATOR, 
                   recommendReGeneratorPerDay,
                   retry_policy=RetryPolicy(initial_interval = 30, backoff_factor=3, max_attempts=3))
graphFlow.add_node(RECOMMENDATION_CONDITIONAL_ROUTING, 
                   conditionalRerouter,
                   retry_policy=RetryPolicy(initial_interval = 30, backoff_factor=3, max_attempts=3))

graphFlow.add_edge(START, RECOMMENDATION_GENERATOR)
graphFlow.add_edge(RECOMMENDATION_GENERATOR, RECOMMENDATION_CRITIC)
graphFlow.add_edge(RECOMMENDATION_GENERATOR, RECOMMENDATION_REGENERATOR)
graphFlow.add_conditional_edges(RECOMMENDATION_REGENERATOR, conditionalRerouter, 
                                {
                                    RECOMMENDATION_CRITIC:RECOMMENDATION_CRITIC,
                                    END:END
                                })
graphFlow.add_edge(RECOMMENDATION_CONDITIONAL_ROUTING, END)
subGraph = graphFlow.compile()

def recommendationSubGraph(state:DesiredCategoriesForOneDay):
    result = subGraph.invoke( {
        'desiredCategoriesForOneDay' : state,
        'activityRecommendationPerDay' :  None,
        'recommendationCriticPerDay' :  None,
        'currenTNumberOfIteration' :  None,
        })
    return {'activityRecommendationPerDay':result['structer_response']}

if __name__ == "__main__":
    # main()
    pass