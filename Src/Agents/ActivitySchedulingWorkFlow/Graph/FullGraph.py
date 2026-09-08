from langgraph.graph import StateGraph, START, END
from ActivitySchedulingWorkFlow.Schemas import GraphState
from ActivitySchedulingWorkFlow.Nodes.ScheduleExtraction import scheduleExtraction
from ActivitySchedulingWorkFlow.Graph.SubGraph import recommendationSubGraph
from ActivitySchedulingWorkFlow.Nodes.Synthesizer import synthersizer


SCHEDULE_EXTRACTION = 'SCHEDULE_EXTRACTION'
SYNTHESIZER = 'SYNTHESIZER'
RECOMMENDATION_SUBGRAPH = 'RECOMMENDATION_SUBGRAPH'
ADD_WORKER_NODES = 'ADD_WORKER_NODES'


def addWorkerNodes(state:GraphState):
    return [Send(RECOMMENDATION_SUBGRAPH, activity) for activity in state['totalDesiredActivities'].ListOfDesiredActivity]

graphFlow = StateGraph(GraphState)
graphFlow.add_node(SCHEDULE_EXTRACTION, scheduleExtraction)
graphFlow.add_node(RECOMMENDATION_SUBGRAPH, recommendationSubGraph)
graphFlow.add_node(ADD_WORKER_NODES, addWorkerNodes)
graphFlow.add_node(SYNTHESIZER, synthersizer)

graphFlow.set_entry_point(SCHEDULE_EXTRACTION)
graphFlow.add_edge(SCHEDULE_EXTRACTION, ADD_WORKER_NODES)
graphFlow.add_edge(RECOMMENDATION_SUBGRAPH, SYNTHESIZER)
graphFlow.add_edge(SYNTHESIZER, END)
fullGraph = graphFlow.compile()

def main():
    pass

if __name__ == "__main__":
    main()
