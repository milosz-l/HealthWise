from langchain_community.chat_models import ChatPerplexity
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os


class KnowledgeChain:
    def __init__(self, source=None):
        self.source = "OpenAI"
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)

        if source is not None:
            self.source = source
            # llm = ChatPerplexity(
            #     model="llama-3.1-sonar-large-128k-online",
            #     pplx_api_key=os.getenv("PERPLEXITYAI_API_KEY"),
            #     temperature=0.0,
            #     model_kwargs={"search_domain_filter": self.source},
            #     # search_domain_filter=self.source,  # Pass as a keyword argument
            # )
            llm = TavilySearchAPIRetriever(
                # k=5,
                include_generated_answer=True,
                include_domains=[self.source],
                # search_depth="advanced",
            )

        KNOWLEDGE_PROMPT_TEMPLATE = (
            f"You are a knowledgebase. Provide general medical information about the following symptoms or conditions, "
            f"referencing professional medical literature specifically from {self.source}. "
            "Include every used citation at the end of the response, formatted as below:\n\n"
            "[1] Title of link1 (https://link1.com)\n"
            "[2] Title of link2 (https://link2.com)\n"
            """etc.
User request: {rephrased_request}
Medical information:"""
        )

        self.chain = llm

    def invoke(self, state):
        return {
            "source_knowledge_pairs": [
                (self.source, self.chain.invoke(state["rephrased_request"]))
            ]
        }
