from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_google_genai import GoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv # used to store secret stuff like API keys or configuration values

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = GoogleGenerativeAI(model="gemini-2.5-flash")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()

user_input = input("Enter : ")
while user_input != "exit":
    # FIX: The messages list needs to contain a HumanMessage object
    agent.invoke({
        "messages": [HumanMessage(content=user_input)]
    })
    user_input = input("Enter : ")
