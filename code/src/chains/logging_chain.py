from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from datetime import datetime
from database import Database


class LoggingChain:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
        self.db = Database()

    def create(self):
        # first, summarize conversation
        summarization_chain = RunnablePassthrough.assign(
            summary=self._summarize_conversation
        )
        # then, classify symptoms based on the summary
        classification_chain = RunnablePassthrough.assign(
            symptoms_categories=self._classify_symptoms
        )
        # finally, save the data
        saving_chain = (
            RunnablePassthrough.assign(
                datetime=self._get_current_datetime,
            )
            | self._save_data
        )
        return summarization_chain | classification_chain | saving_chain

    def _get_current_datetime(self, state):
        return datetime.now().isoformat()

    def _summarize_conversation(self, state):
        prompt_template = PromptTemplate.from_template(
            """
Summarize the user's symptoms from the following conversation into one sentence. The summary should be in English.

Conversation:
{conversation_history}

Summary:
"""
        )
        chain = prompt_template | self.llm | StrOutputParser()
        return chain.invoke({"conversation_history": state["conversation_history"]})

    def _classify_symptoms(self, state):
        prompt_template = PromptTemplate.from_template(
            """
Classify the following medical summary into one or more of the following categories. Return the applicable categories as a comma-separated list:

List of categories:
General Symptoms, Respiratory Symptoms, Cardiovascular Symptoms, Gastrointestinal Symptoms, Neurological Symptoms, Musculoskeletal Symptoms, Dermatological Symptoms, Psychological Symptoms, Endocrine Symptoms, Urinary Symptoms, Reproductive Symptoms, ENT (Ear/Nose/Throat) Symptoms, Ophthalmological Symptoms, None

Example response:
General Symptoms, Neurological Symptoms



Now, provide the categories for the following summary.

Summary of conversation:
{summary}

Categories for given summary:
"""
        )
        chain = prompt_template | self.llm | StrOutputParser()
        response = chain.invoke({"summary": state["summary"]})
        categories = [category.strip() for category in response.split(",")]
        return categories

    def _save_data(self, state):
        self.db.save_conversation(
            {
                "conversation_id": state["conversation_id"],
                "conversation": state["conversation_history"],
                "conversation_id": state["conversation_id"],
                "location": state["location"],
                "datetime": state["datetime"],
                "summary": state["summary"],
                "symptoms_categories": state["symptoms_categories"],
            }
        )
