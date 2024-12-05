from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os


class KnowledgeChain:
    def __init__(self, source):
        KNOWLEDGE_PROMPT_TEMPLATE = "You are a knowledgebase. Provide general medical information about the following symptoms or conditions, referencing professional medical literature specifically from " + source + """.
User request: {rephrased_request}
Medical information:"""
        llm = ChatPerplexity(model="llama-3.1-sonar-small-128k-online", pplx_api_key=os.getenv("PERPLEXITYAI_API_KEY"))

        self.source = source
        self.chain = PromptTemplate.from_template(KNOWLEDGE_PROMPT_TEMPLATE) | llm #| StrOutputParser()


    def invoke(self, state):
        return {"source_knowledge_pairs": [(self.source, self.chain.invoke(state))]}

