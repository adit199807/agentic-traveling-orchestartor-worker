from langgraph.graph import StateGraph, START, END
from ActivitySchedulingWorkFlow.Schemas import SubGraphState
from ActivitySchedulingWorkFlow.Nodes.SubNodeRecommendationGenerator import recommendationGenerator
from ActivitySchedulingWorkFlow.Nodes.SubNodeCriticRecommendation import criticRecommendation
from ActivitySchedulingWorkFlow.Nodes.SubNodeRecommendationRegenerator import recommendReGeneratorPerDay
from ActivitySchedulingWorkFlow.Nodes.SubNodeConditionalRerouter import conditionalRerouter
from ActivitySchedulingWorkFlow.Schemas import GraphState


RECOMMENDATION_GENERATOR = 'RECOMMENDATION_GENERATOR'
RECOMMENDATION_CRITIC = 'RECOMMENDATION_CRITIC'
RECOMMENDATION_REGENERATOR = 'RECOMMENDATION_REGENERATOR'
RECOMMENDATION_CONDITIONAL_ROUTING = 'RECOMMENDATION_CONDITIONAL_ROUTING'

graphFlow = StateGraph(SubGraphState)
graphFlow.add_node(RECOMMENDATION_GENERATOR, recommendationGenerator)
graphFlow.add_node(RECOMMENDATION_CRITIC, criticRecommendation)
graphFlow.add_node(RECOMMENDATION_REGENERATOR, recommendReGeneratorPerDay)
graphFlow.add_node(RECOMMENDATION_CONDITIONAL_ROUTING, conditionalRerouter)

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

def recommendationSubGraph(state:SubGraphState):
    result = subGraph.invoke({'desiredCategoriesForOneDay':state['desiredCategoriesForOneDay']})
    return {'activityRecommendationPerDay':result['structer_response']}

if __name__ == "__main__":
    # main()
    pass