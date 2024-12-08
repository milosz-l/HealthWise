from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch


class ChatbotChain:
    REPHRASE_PROMPT_TEMPLATE = """
You are a medical assistant helper. Your task is to take the user's medical request and rephrase it into a concise, unpersonolized, normalized query in English that focuses on symptoms and diseases. If user request does not relate to a medical condition, return UNRELATED only.
User request: {user_request}
"""

    ANSWER_PROMPT_TEMPLATE = """You are a medical assistant. Your task is to address the user's medical request by providing suggestions using the language in which the user's request is written, utilizing knowledge retrieved from medical sources. As you craft your response, carefully integrate and organize the retrieved knowledge to ensure a logical flow. When referencing these sources, insert links in markdown format and maintain strict sequential numbering based on the order they are introduced in your response. Before finalizing, review your response to confirm all links are present and the numbering is correct with no numbers skipped.
Retrieved medical knowledge:
<RETRIVED_MEDICAL_KNOWLEDGE>
{aggregated_knowledge}
</RETRIVED_MEDICAL_KNOWLEDGE>
User request (written in the language to be used for the answer): {user_request}
Answer with suggestions (if the user request is in English answer in English):"""

    TRANSLATE_UNRELATED_PROMPT_TEMPLATE = """
You are a translator. Translate the message below using the language in which the user's request is written.
Message to translate: It seems your request does not relate to a medical condition. Please try again with a focus on symptoms or diseases.
User request: {user_request}

Translated message:
"""

    def create(self):
        answer_llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        rephrase_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
        return RunnableBranch(
            (
                lambda x: x["aggregated_knowledge"] != "",
                {
                    "answer": PromptTemplate.from_template(self.ANSWER_PROMPT_TEMPLATE)
                    | answer_llm
                    | StrOutputParser()
                },
            ),
            lambda x: self._rephrase_request(x, rephrase_llm),
        )

    def _rephrase_request(self, state, llm):
        rephrased_request = (
            PromptTemplate.from_template(self.REPHRASE_PROMPT_TEMPLATE)
            | llm
            | StrOutputParser()
        ).invoke(state)

        if rephrased_request == "UNRELATED":
            return {
                "answer": (
                    PromptTemplate.from_template(
                        self.TRANSLATE_UNRELATED_PROMPT_TEMPLATE
                    )
                    | llm
                    | StrOutputParser()
                ).invoke(state)
            }
        else:
            return {"rephrased_request": rephrased_request}
