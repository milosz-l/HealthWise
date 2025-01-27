from dotenv import load_dotenv
load_dotenv()

import unittest

from langchain_openai import ChatOpenAI

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from chains.aggregation_chain import AggregationChain
from chains.chatbot_chain import ChatbotChain
from chains.knowledge_chain import KnowledgeChain
from chains.logging_chain import LoggingChain
from chains.validation_chain import ValidationChain


# Test scenario for ValidationChain
class TestValidationChain(unittest.TestCase):
    def test_format_conversation_history(self):
        chain_class = ValidationChain()
        state = {
            "conversation_history": [
                {"user": "Hello"},
                {"bot": "Hi there!"},
                {"user": "What's the time?"},
            ]
        }
        result = chain_class._format_conversation_history(state)
        self.assertEqual(result, "0. User: Hello\n1. Bot: Hi there!\n2. User: What's the time?")

    def test_invoke_unrelated_message(self):
        chain_class = ValidationChain()
        chain = chain_class.create()
        state = {
            "conversation_history": [
                {"user": "Hello"},
                {"bot": "Hi there!"},
                {"user": "What's the time?"},
            ]
        }
        result = chain.invoke(state)
        self.assertEqual(result["answer"], chain_class.UNRELATED_REQUEST_MESSAGE)

    def test_invoke_complete(self):
        chain = ValidationChain().create()
        state = {
            "conversation_history": [
                {"user": "I have been experiencing stomach pain for the past three days. My temperature is normal, and I don't have any allergies or take any medications."},
            ]
        }
        result = chain.invoke(state)
        self.assertNotIn("followup_question", result)
        self.assertEqual(result["processing_state"], ["Analyzing user's medical query..."])

    def test_invoke_incomplete(self):
        chain = ValidationChain().create()
        state = {
            "conversation_history": [
                {"user": "I have been experiencing stomach pain for the past three days."}
            ]
        }
        result = chain.invoke(state)
        self.assertIn("followup_question", result)


# Test scenario for ChatbotChain
class TestChatbotChain(unittest.TestCase):
    def test_format_conversation_history(self):
        chain_class = ChatbotChain()
        state = {
            "conversation_history": [
                {"user": "Hello"},
                {"bot": "Hi there!"},
                {"user": "What's the time?"},
            ]
        }
        result = chain_class._format_conversation_history(state)
        self.assertEqual(result, "0. User: Hello\n1. Bot: Hi there!\n2. User: What's the time?")

    def test_rephrase_request(self):
        chain_class = ChatbotChain()
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
        state = {
            "aggregated_knowledge": "",
            "conversation_history": [{"user": "I have a headache."}]
        }
        result = chain_class._rephrase_request(state, llm)
        self.assertIn("rephrased_request", result)
        self.assertNotIn("answer", result)
        self.assertEqual(result["processing_state"], ["Retrieving medical information from knowledge sources..."])

    def test_invoke(self):
        chain = ChatbotChain().create()
        state = {
            "aggregated_knowledge": "According to the authoritative medical sources, the user may have a diarrhea :(",
            "conversation_history": [{"user": "I have a stomach pain."}]
        }
        result = chain.invoke(state)
        self.assertIn("answer", result)
        self.assertEqual(result["processing_state"], ["FINISH"])


# Test scenario for KnowledgeChain
class TestKnowledgeChain(unittest.TestCase):
    def test_invoke(self):
        chain = KnowledgeChain(source="https://www.nhs.uk")
        state = {
            "rephrased_request": "Headache, high temperature",
        }
        result = chain.invoke(state)
        self.assertIn("source_knowledge_pairs", result)
        self.assertEqual(result["processing_state"], ["Retrieved medical information from [https://www.nhs.uk](https://www.nhs.uk). Aggregating knowledge..."])


# Test scenario for AggregationChain
class TestAggregationChain(unittest.TestCase):
    def test_format_source_knowledge_pairs(self):
        chain_class = AggregationChain()
        state = {
            "source_knowledge_pairs": [
                ("source1", "knowledge1"),
                ("source2", "knowledge2")
            ]
        }
        result = chain_class._format_source_knowledge_pairs(state)
        self.assertIn("Knowledge agent for: source1", result)
        self.assertIn("Medical information: knowledge1", result)
        self.assertIn("Knowledge agent for: source2", result)
        self.assertIn("Medical information: knowledge2", result)

    def test_invoke(self):
        chain = AggregationChain().create()
        state = {
            "source_knowledge_pairs": [
                ("source1", "Knowledge1 is a test data for case for the source1 [1]"),
                ("source2", "Knowledge2 is a test data for case for the source1 [2]")
            ]
        }
        result = chain.invoke(state)
        self.assertIn("aggregated_knowledge", result)
        self.assertEqual(result["processing_state"], ["Knowledge aggregated. Generating response..."])


# Test scenario for LoggingChain
class TestLoggingChain(unittest.TestCase):
    def test_summarize_conversation(self):
        chain_class = LoggingChain(ignore_db=True)
        state = {
            "conversation_history": [
                {"user": "I have a heart pain."},
                {"bot": "Anything else?"},
                {"user": "My temperature is high also."},
            ]
        }
        result = chain_class._summarize_conversation(state)
        self.assertIn("heart", result)
        self.assertIn("temperature", result)

    def test_classify_symptoms(self):
        chain_class = LoggingChain(ignore_db=True)
        state = {"summary": "I have a headache and don't feel the left handfingers."}
        result = chain_class._classify_symptoms(state)
        self.assertIn("Neurological Symptoms", result)


# Run all tests
if __name__ == "__main__":
    unittest.main()