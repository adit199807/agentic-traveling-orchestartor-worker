from ActivitySchedulingWorkFlow.Graph.FullGraph import fullGraph

def main():
    print("============================Flight Agent at Service============================")
    thread_connfig = {"configurable": {"thread_id": "manager_session_456"}}
    try: 
        response = fullGraph.invoke(input={'userInput':''})
        print(response)
    except Exception as e:
            print(f"Caught Expected Error: {e}\n")
            state_snapshot = flightAgent.get_state(thread_connfig)
            messages = state_snapshot.values.get("messages", [])

if __name__ == "__main__":
    print("This is your Flight Agent!")
    main()
