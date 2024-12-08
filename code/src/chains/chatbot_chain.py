from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch


class ChatbotChain:
    REPHRASE_PROMPT_TEMPLATE = """You are a medical assistant helper. Your task is to take the user's medical request and rephrase it into a concise, unpersonolized, normalized query in English that focuses on symptoms and diseases. If user request does not relate to a medical condition, return UNRELATED only.
User request: {user_request}
Rephrased request or UNRELATED:"""

    ANSWER_PROMPT_TEMPLATE = """You are a medical assistant. Your task is to take the user's medical request and provide the user suggestions in original request language that the user request was written in, utilizing knowledge retrieved from medical sources, referencing sources if possible.
User request: {user_request}
Retrieved medical knowledge: {aggregated_knowledge}
Answer with suggestions:"""

    TRANSLATE_UNRELATED_PROMPT_TEMPLATE = """You are a translator. Translate the message below using the language in which the user's request is written.
Message to translate: It seems your request does not relate to a medical condition. Please try again with a focus on symptoms or diseases.
User request: {user_request}"""

    def create(self):
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
        return RunnableBranch(
            (
                lambda x: x["aggregated_knowledge"] != "",
                {
                    "answer": PromptTemplate.from_template(self.ANSWER_PROMPT_TEMPLATE)
                    | llm
                    | StrOutputParser()
                },
            ),
            lambda x: self._rephrase_request(x, llm),
        )

    def _rephrase_request(self, x, llm):
        rephrased_request = (
            PromptTemplate.from_template(self.REPHRASE_PROMPT_TEMPLATE)
            | llm
            | StrOutputParser()
        ).invoke(x)

        if rephrased_request == "UNRELATED":
            return {
                "answer": (
                    PromptTemplate.from_template(
                        self.TRANSLATE_UNRELATED_PROMPT_TEMPLATE
                    )
                    | llm
                    | StrOutputParser()
                ).invoke(x)
            }
        else:
            return {"rephrased_request": rephrased_request}
