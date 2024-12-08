from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


class AggregationChain:
    AGGREGATION_PROMPT_TEMPLATE = """"You are a knowledge aggregator. Aggregate the medical knowledge retrieved from different sources to create an article summarizing all of them, providing the most important information from each source. "Reference the provided sources, attaching used citations from knowledge at the end in below format:
\n
[1] Title of link1 (https://link1.com)
[2] Title of link2 (https://link2.com)
...etc.

Medical information with sources:
<MEDICAL_KNOWLEDGE>
{formatted_source_knowledge_pairs}
</MEDICAL_KNOWLEDGE>
Aggregated medical information:"""

    def create(self):
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
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
            formatted_entry = f"Source: {source}\nKnowledge: {knowledge}\n"
            formatted_entries.append(formatted_entry)
        return "\n".join(formatted_entries)
