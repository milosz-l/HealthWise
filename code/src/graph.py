from chains.chatbot_chain import ChatbotChain
from chains.knowledge_chain import KnowledgeChain

from langgraph.graph import END, StateGraph
from typing import TypedDict


class MedicalState(TypedDict):
    user_request: str
    refrased_request: str
    knowledge: str
    answer: str

class MedicalGraph:
    def _request_answered(self, state: MedicalState):
        if state["answer"] == "":
            return False
        else:
            return True

    def create(self):
        graph = StateGraph(MedicalState)

        graph.add_node("chatbot_agent", ChatbotChain().create())
        graph.add_node("knowledge_agent", KnowledgeChain().create())

        graph.add_conditional_edges("chatbot_agent", self._request_answered, {True: END, False: "knowledge_agent"})
        graph.add_edge("knowledge_agent", "chatbot_agent")

        graph.set_entry_point("chatbot_agent")

        return graph.compile()
