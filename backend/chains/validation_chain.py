from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda


class ValidationChain:
    UNRELATED_REQUEST_MESSAGE = "It seems your request does not relate to a medical condition. Please provide more specific information about your symptoms or relevant medical details."

    VALIDATION_PROMPT_TEMPLATE = """Task:
Analyze the latest user request (written in any language) in the context of the conversation history to determine:
1. If it is related to a medical condition.
2. If additional information is needed, or if the required information is complete.

Instructions:
- Return "UNRELATED" if the last user question is not describing the medical condition.
- If essential information is missing, generate a follow-up question that asks for all required details without incorporating your own thoughts or considerations.
- Return "COMPLETE" if all required details are provided.

List of Required Information:
- Body Temperature
- Duration of Symptoms
- Medications Currently Being Taken
- Any Known Allergies

Example follow-up question requesting any missing Required Information, given that the user mentioned in conversation he is experiencing headaches and have taken ibuprofen:
I'm sorry you're experiencing headaches. Could you please provide more details, such as your current body temperature, the duration of your symptoms, and whether you have any known allergies?

Conversation History with latest user request (in language used by the user):
<CONVERSATION_HISTORY>
{conversation_history}
</CONVERSATION_HISTORY>

Follow-up question text (in English), or UNRELATED, or COMPLETE:
"""

    TRANSLATE_PROMPT_TEMPLATE = """
You are a translator from English to any language. Translate the message below using the language in which the user's request is written:
{message_to_translate}

Text of the message translated to language in which "{user_request}" is written (if English is used, don't translate the message):
"""

    def create(self):
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)
        translation_llm = ChatOpenAI(model_name="gpt-4o", temperature=0.1)
        return {
            "message_to_translate": (
                {"conversation_history": self._format_conversation_history}
                | PromptTemplate.from_template(self.VALIDATION_PROMPT_TEMPLATE)
                | llm
                | StrOutputParser()
            ),
            "user_request": RunnableLambda(
                lambda x: x["conversation_history"][-1]["user"]
            ),
        } | RunnableBranch(
            (
                lambda x: x["message_to_translate"] == "UNRELATED",
                {
                    "answer": {
                        "message_to_translate": RunnableLambda(
                            lambda x: self.UNRELATED_REQUEST_MESSAGE
                        ),
                        "user_request": RunnableLambda(lambda x: x["user_request"]),
                    }
                    | PromptTemplate.from_template(self.TRANSLATE_PROMPT_TEMPLATE)
                    | translation_llm
                    | StrOutputParser()
                },
            ),
            (
                lambda x: x["message_to_translate"] == "COMPLETE",
                {"processing_state": RunnableLambda(lambda x: ["Analyzing user's medical query..."])},
            ),
            {
                "followup_question": PromptTemplate.from_template(self.TRANSLATE_PROMPT_TEMPLATE)
                | translation_llm
                | StrOutputParser()
            },
        )

    def _format_conversation_history(self, state):
        formatted_history = []
        for idx, entry in enumerate(state["conversation_history"]):
            if "user" in entry and entry["user"]:
                formatted_history.append(f"{idx}. User: {entry['user']}")
            elif "bot" in entry:
                formatted_history.append(f"{idx}. Bot: {entry['bot']}")
        return "\n".join(formatted_history)
