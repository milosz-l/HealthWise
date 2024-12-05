from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class KnowledgeChain:
    def __init__(self, source):
        KNOWLEDGE_PROMPT_TEMPLATE = "You are a knowledgebase. Provide general medical information about the following symptoms or conditions, referencing professional medical literature specifically from " + source + """.
        User request: {rephrased_request}
        Medical information:"""
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)

        self.source = source
        self.chain = PromptTemplate.from_template(KNOWLEDGE_PROMPT_TEMPLATE) | llm | StrOutputParser()


    def invoke(self, state):
        return {"source_knowledge_pairs": [(self.source, self.chain.invoke(state))]}

