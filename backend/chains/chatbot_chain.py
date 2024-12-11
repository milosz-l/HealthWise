from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda


class ChatbotChain:
    REPHRASE_PROMPT_TEMPLATE = """
You are a medical assistant helper. Your task is to take the conversation between user and medical chatbot and rephrase it into a concise, unpersonolized, normalized query in English that focuses on symptoms and diseases.
Previous conversation history with latest user request:
<CONVERSATION_HISTORY>
{conversation_history}
<CONVERSATION_HISTORY>
Rephrased query:
"""

    ANSWER_PROMPT_TEMPLATE = """You are a medical assistant. Your task is to address the user's medical request by providing a comprehensive range of suggestions using the language in which the user's requests and the whole conversation is written, utilizing knowledge retrieved from medical sources. As you craft your response, carefully integrate and organize the retrieved knowledge to ensure a logical flow. When referencing these sources, insert links in markdown format and assign your own sequential numbering ([1], [2], [3], ...; not like [1.2]) based on the order they are introduced in your response. Before finalizing, review your response to ensure all links are present and the numbering is correct, with no numbers skipped. If tavily.com is returned as a knowledge link, do not cite it; instead, use another source.
Retrieved medical knowledge:
<RETRIVED_MEDICAL_KNOWLEDGE>
{aggregated_knowledge}
</RETRIVED_MEDICAL_KNOWLEDGE>

Answer example for the user request "I've been experiencing severe headaches and a high temperature. Can you help?":
<ANSWER_EXAMPLE>
I'm sorry to hear that you're experiencing severe headaches and a high temperature. Here are a few suggestions based on the medical information I've found that might help you:

1. **Suggestion 1**: Description or recommendation based on the aggregated_knowledge, with or without the source reference[1].
2. **Suggestion 2**: Another tip or piece of advice based on the aggregated_knowledge, with or without the source reference[2].
...

For more details, you can check out these sources:

[1] [Title of the first citation](https://link1.com)
[2] [Title of the second citation](https://link2.com)
</ANSWER_EXAMPLE>

Previous conversation history with latest user request (written in the language to be used for the answer):
<CONVERSATION_HISTORY>
{conversation_history}
<CONVERSATION_HISTORY>

Answer with suggestions (if the previous conversation is in English answer in English):
"""

    def create(self):
        answer_llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)
        rephrase_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
        return RunnableBranch(
            (
                lambda x: x["aggregated_knowledge"] != "",
                {
                    "answer": {
                        "aggregated_knowledge": RunnableLambda(
                            lambda x: x["aggregated_knowledge"]
                        ),
                        "conversation_history": self._format_conversation_history,
                    }
                    | PromptTemplate.from_template(self.ANSWER_PROMPT_TEMPLATE)
                    | answer_llm
                    | StrOutputParser(),
                    "processing_state": RunnableLambda(lambda x: ["FINISH"])
                },
            ),
            lambda x: self._rephrase_request(x, rephrase_llm),
        )

    def _rephrase_request(self, state, llm):
        rephrased_request = (
            self._format_conversation_history
            | PromptTemplate.from_template(self.REPHRASE_PROMPT_TEMPLATE)
            | llm
            | StrOutputParser()
        ).invoke(state)
        return {
            "rephrased_request": rephrased_request,
            "processing_state": ["Retrieving medical information from knowledge sources..."]
        }

    def _format_conversation_history(self, state):
        formatted_history = []
        for idx, entry in enumerate(state["conversation_history"]):
            if "user" in entry and entry["user"]:
                formatted_history.append(f"{idx}. User: {entry['user']}")
            elif "bot" in entry:
                formatted_history.append(f"{idx}. Bot: {entry['bot']}")
        return "\n".join(formatted_history)
