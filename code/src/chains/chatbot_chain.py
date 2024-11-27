from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch


class ChatbotChain:
    REPHRASE_PROMPT_TEMPLATE = """You are a medical assistant helper. Your task is to take the user's medical request and rephrase it into a concise, normalized query that focuses on symptoms and diseases.
        User request: {user_request}
        Rephrased request:"""

    ANSWER_PROMPT_TEMPLATE = """You are a medical assistant. Your task is to take the user's medical request and provide the user suggestions in original request language, utilizing knowledge retrieved from medical sources, referencing sources if possible.
        User request: {user_request}
        Retrieved medical knowledge: {knowledge}
        Answer with suggestions:"""

    def create(self):
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
        return RunnableBranch(
            (lambda x: x["knowledge"] == "", { "refrased_request": PromptTemplate.from_template(self.REPHRASE_PROMPT_TEMPLATE) | llm | StrOutputParser() }),
            lambda x: { "answer": (PromptTemplate.from_template(self.ANSWER_PROMPT_TEMPLATE) | llm | StrOutputParser()).invoke(input=x) }
        )

