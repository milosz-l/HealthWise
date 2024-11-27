from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class KnowledgeChain:
    KNOWLEDGE_PROMPT_TEMPLATE = """You are knowledgebase. Provide general medical information about the following symptoms or conditions, referencing professional medical literature.
        User request: {refrased_request}
        Medical information:"""

    def create(self):
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
        return { "knowledge": PromptTemplate.from_template(self.KNOWLEDGE_PROMPT_TEMPLATE) | llm | StrOutputParser() }
