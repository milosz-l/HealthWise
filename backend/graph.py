from chains.validation_chain import ValidationChain
from chains.chatbot_chain import ChatbotChain
from chains.knowledge_chain import KnowledgeChain
from chains.aggregation_chain import AggregationChain
from chains.logging_chain import LoggingChain

from langgraph.graph import END, StateGraph
from typing import Annotated, TypedDict, List
from operator import add
import os


class MedicalState(TypedDict):
    followup_question: str
    rephrased_request: str
    source_knowledge_pairs: Annotated[List[tuple[str, str]], add]
    aggregated_knowledge: str
    answer: str
    conversation_id: str
    location: str
    conversation_history: List[dict]
    summary: str
    symptoms_categories: List[str]
    datetime: str
    processing_state: Annotated[List[str], add]


class MedicalGraph:
    knowledge_agents = [
        "knowledge_agent_nhs",
        "knowledge_agent_medlineplus",
        "knowledge_agent_cdc",
    ]

    def _followup_question_routing(self, state: MedicalState):
        if state["followup_question"] == "" and state["answer"] == "":
            return "chatbot_agent"
        else:
            return END

    def _request_answered_routing(self, state: MedicalState):
        if state["answer"] == "":
            return self.knowledge_agents
        else:
            return "logging_agent"

    def create(self):
        graph = StateGraph(MedicalState)

        graph.add_node("validation_agent", ValidationChain().create())
        graph.add_node("chatbot_agent", ChatbotChain().create())
        graph.add_node("aggregation_agent", AggregationChain().create())
        graph.add_node("logging_agent", LoggingChain().create())
        if os.getenv("TAVILY_API_KEY"):
            graph.add_node(
                "knowledge_agent_medlineplus",
                KnowledgeChain("https://medlineplus.gov").invoke,
            )
            graph.add_node(
                "knowledge_agent_nhs",
                KnowledgeChain("https://www.nhs.uk").invoke,
            )
            graph.add_node(
                "knowledge_agent_cdc",
                KnowledgeChain("https://www.cdc.gov").invoke,
            )
        else:
            self.knowledge_agents = ["knowledge_agent_openai"]
            graph.add_node("knowledge_agent_openai", KnowledgeChain().invoke)

        graph.add_conditional_edges("validation_agent", self._followup_question_routing)
        graph.add_conditional_edges("chatbot_agent", self._request_answered_routing)
        graph.add_edge(self.knowledge_agents, "aggregation_agent")
        graph.add_edge("aggregation_agent", "chatbot_agent")
        graph.add_edge("logging_agent", END)

        graph.set_entry_point("validation_agent")

        return graph.compile()
