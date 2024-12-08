from langchain_community.chat_models import ChatPerplexity
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
import os, json


class KnowledgeChain:
    def __init__(self, source=None):
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
        self.source = "OpenAI"
        if source != None:
            llm = ChatPerplexity(
                model="llama-3.1-sonar-small-128k-online",
                pplx_api_key=os.getenv("PERPLEXITYAI_API_KEY"),
            )
            self.source = source

        KNOWLEDGE_PROMPT_TEMPLATE = (
            "You are a knowledgebase. Provide general medical information about the following symptoms or conditions, referencing professional medical literature specifically from "
            + self.source
            + """.
User request: {rephrased_request}
Medical information:"""
        )

        self.chain = PromptTemplate.from_template(KNOWLEDGE_PROMPT_TEMPLATE) | llm

    def invoke(self, state):
        return {"source_knowledge_pairs": [(self.source, self.chain.invoke(state))]}


class PerplexityOutputParser(BaseOutputParser[str]):

    def parse(self, json_str):
        data = json.loads(json_str)
        content = data.get("content", "")
        citations = data.get("citations", [])
        formatted_content = content + "\n\n"
        for index, citation in enumerate(citations, start=1):
            formatted_content += f"[{index}] {citation}\n"
        return formatted_content
