from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_openai import ChatOpenAI


class KnowledgeChain:
    def __init__(self, source=None):
        self.source = "OpenAI"
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)
        if source is not None:
            self.source = source
            llm = TavilySearchAPIRetriever(
                include_generated_answer=True,
                include_domains=[self.source],
                search_depth="advanced",
            )
        self.chain = llm | self._format_tavily_response

    def _format_tavily_response(self, retrieved_documents):
        formatted_response = []
        for index, document in enumerate(retrieved_documents):
            content = document.page_content
            source = document.metadata["source"]
            formatted_response.append(f"{content}\n[{index + 1}] {source}\n")
        return "\n".join(formatted_response)

    def invoke(self, state):
        try:
            retrieved_knowledge = self.chain.invoke(state["rephrased_request"])
        except:  # TODO: fix tavily error
            pass
        return {
            "source_knowledge_pairs": [
                (self.source, retrieved_knowledge)
            ],
            "processing_state": [f"Retrieved medical information from [{self.source}]({self.source}). Aggregating knowledge..."]
        }
