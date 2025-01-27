from dotenv import load_dotenv
load_dotenv()

import unittest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from graph import MedicalGraph


# Test scenario for the entire MedicalGraph
class TestMedicalGraph(unittest.TestCase):
    def test_unrelated_message(self):
        graph = MedicalGraph().create()
        state = {
            "rephrased_request": "",
            "source_knowledge_pairs": [],
            "aggregated_knowledge": "",
            "followup_question": "",
            "answer": "",
            "conversation_id": "id",
            "location": "",
            "conversation_history": [{"user": "Give me a cake recipe."}],
            "summary": "",
            "symptoms_categories": [],
            "datetime": "",
            "processing_state": [],
        }
        result = graph.invoke(state)
        self.assertEqual(result["followup_question"], "")
        self.assertNotEqual(result["answer"], "")
        self.assertEqual(result["processing_state"], [])

    def test_followup_question(self):
        graph = MedicalGraph().create()
        state = {
            "rephrased_request": "",
            "source_knowledge_pairs": [],
            "aggregated_knowledge": "",
            "followup_question": "",
            "answer": "",
            "conversation_id": "id",
            "location": "",
            "conversation_history": [{"user": "I have a stomach pain and high temperature."}],
            "summary": "",
            "symptoms_categories": [],
            "datetime": "",
            "processing_state": [],
        }
        result = graph.invoke(state)
        self.assertNotEqual(result["followup_question"], "")
        self.assertEqual(result["answer"], "")
        self.assertEqual(result["processing_state"], [])

    def test_final_response(self):
        graph = MedicalGraph().create()
        state = {
            "rephrased_request": "",
            "source_knowledge_pairs": [],
            "aggregated_knowledge": "",
            "followup_question": "",
            "answer": "",
            "conversation_id": "id",
            "location": "",
            "conversation_history": [{"user": "I have been experiencing stomach pain for the past three days. My temperature is normal, and I don't have any allergies or take any medications."}],
            "summary": "",
            "symptoms_categories": [],
            "datetime": "",
            "processing_state": [],
        }
        result = graph.invoke(state)
        self.assertEqual(result["followup_question"], "")
        self.assertNotEqual(result["answer"], "")
        self.assertNotEqual(result["processing_state"], [])


# Run all tests
if __name__ == "__main__":
    unittest.main()