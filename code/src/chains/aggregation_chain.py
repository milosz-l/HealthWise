from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


class AggregationChain:
    AGGREGATION_PROMPT_TEMPLATE = """You are a medical information aggregator. Aggregate the medical information retrieved from different knowledge agents to create an article summarizing all of them. At the end of your response, reference links used in your final answer separately for each knowledge agent. Example citation format:

- Title of link1 from knowledge agent 1 [1.1](https://link1.com)
- Title of link2 from knowledge agent 1 [1.2](https://link2.com)
- Title of link1 from knowledge agent 2 [2.1](https://link1.com)
- Title of link2 from knowledge agent 2 [2.2](https://link2.com)
...etc.

Medical information with sources:
<MEDICAL_KNOWLEDGE>
{formatted_source_knowledge_pairs}
</MEDICAL_KNOWLEDGE>

Aggregated medical information:
"""

    def create(self):
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)
        return {
            "aggregated_knowledge": {
                "formatted_source_knowledge_pairs": self._format_source_knowledge_pairs
            }
            | PromptTemplate.from_template(self.AGGREGATION_PROMPT_TEMPLATE)
            | llm
            | StrOutputParser()
        }

    def _format_source_knowledge_pairs(self, state):
        formatted_entries = []
        for source, knowledge in state["source_knowledge_pairs"]:
            formatted_entry = (
                f"Knowledge agent for: {source}\nMedical information: {knowledge}\n"
            )
            formatted_entries.append(formatted_entry)
        return "\n---\n".join(formatted_entries)
