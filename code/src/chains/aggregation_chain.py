from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatPerplexity
import os


class AggregationChain:
    AGGREGATION_PROMPT_TEMPLATE = """You are a knowledge aggregator. Aggregate the medical knowledge retrieved from different sources to create an article summarizing all of them, providing the most important information from each source.
        Medical information with sources:
        <MEDICAL_KNOWLEDGE>
        {formatted_source_knowledge_pairs}
        </MEDICAL_KNOWLEDGE>
        Aggregated medical information:"""

    def create(self):
        llm = ChatPerplexity(model="gpt-4o-mini", pplx_api_key=os.getenv("PERPLEXITYAI_API_KEY"))
        return {"aggregated_knowledge":
                {"formatted_source_knowledge_pairs": self._format_source_knowledge_pairs}
                | PromptTemplate.from_template(self.AGGREGATION_PROMPT_TEMPLATE)
                | llm
                | StrOutputParser()}

    def _format_source_knowledge_pairs(self, state):
        formatted_entries = []
        for source, knowledge in state["source_knowledge_pairs"]:
            formatted_entry = f"Source: {source}\nKnowledge: {knowledge}\n"
            formatted_entries.append(formatted_entry)
        return "\n".join(formatted_entries)
