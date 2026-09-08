import operator
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from typing import Any, TypedDict
from Agents.ActivitySchedulingWorkFlow.Schemas import GraphState
from Agents.ActivitySchedulingWorkFlow.Nodes.ScheduleExtraction import scheduleExtraction
from Agents.ActivitySchedulingWorkFlow.Graph.SubGraph import recommendationSubGraph
from Agents.ActivitySchedulingWorkFlow.Nodes.Synthesizer import synthersizer


SCHEDULE_EXTRACTION = 'SCHEDULE_EXTRACTION'
SYNTHESIZER = 'SYNTHESIZER'
RECOMMENDATION_SUBGRAPH = 'RECOMMENDATION_SUBGRAPH'
ADD_WORKER_NODES = 'ADD_WORKER_NODES'


def addWorkerNodes(state:GraphState):
    return [Send(RECOMMENDATION_SUBGRAPH, acitivty) for acitivty in state['totalDesiredActivities'].ListOfDesiredActivity]

graphFlow = StateGraph(GraphState)
graphFlow.add_node(SCHEDULE_EXTRACTION, scheduleExtraction)
graphFlow.add_node(RECOMMENDATION_SUBGRAPH, recommendationSubGraph)
graphFlow.add_node(ADD_WORKER_NODES, addWorkerNodes)
graphFlow.add_node(SYNTHESIZER, synthersizer)

graphFlow.set_entry_point(SCHEDULE_EXTRACTION)
graphFlow.add_conditional_edges(SCHEDULE_EXTRACTION, addWorkerNodes, [RECOMMENDATION_SUBGRAPH])
graphFlow.add_edge(RECOMMENDATION_SUBGRAPH, SYNTHESIZER)
graphFlow.add_edge(SYNTHESIZER, END)
fullGraph = graphFlow.compile()

def main():
    result = fullGraph.invoke({
        'userInput' : """Hi am planning ofr 3 days in Tokyo. I would like to schedule activities of categories Food, Nature and Views. My budget is 500 USD""",
        'totalDesiredActivities' : None,
        'activityAgentResponse' : None,
        'activityRecommendationPerDay' : None,
        'currentDesiredActivitiesToParse' : None
    })

if __name__ == "__main__":
    main()
