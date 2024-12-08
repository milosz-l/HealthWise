from langchain_community.chat_models import ChatPerplexity
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os


class KnowledgeChain:
    def __init__(self, source=None):
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)
        self.source = "OpenAI"
        if source != None:
            llm = ChatPerplexity(
                model="llama-3.1-sonar-large-128k-online",
                pplx_api_key=os.getenv("PERPLEXITYAI_API_KEY"),
            )
            self.source = source

        KNOWLEDGE_PROMPT_TEMPLATE = (
            "You are a knowledgebase. Provide general medical information about the following symptoms or conditions, referencing professional medical literature specifically from "
            + self.source
            + ". Include every used citation at the end of the response, formatted as below:\n\n"
            + "[1] Title of link1 (https://link1.com)\n"
            + "[2] Title of link2 (https://link2.com)\n"
            + """etc.
User request: {rephrased_request}
Medical information:"""
        )

        self.chain = (
            PromptTemplate.from_template(KNOWLEDGE_PROMPT_TEMPLATE)
            | llm
            | StrOutputParser()
        )

    def invoke(self, state):
        return {"source_knowledge_pairs": [(self.source, self.chain.invoke(state))]}
