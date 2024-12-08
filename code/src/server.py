from dotenv import load_dotenv

load_dotenv()

from graph import MedicalGraph

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid
from typing import List

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = MedicalGraph().create()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.post("/")
async def ask(user_request, location: str):
    def event_stream(user_request: str, location: str):
        conversation_id = str(uuid.uuid4())
        initial_state = {
            "user_request": user_request,
            "rephrased_request": "",
            "source_knowledge_pairs": [],
            "aggregated_knowledge": "",
            "answer": "",
            "conversation_id": conversation_id,
            "location": location,
            "conversation_history": [{"user": user_request}],
            "summary": "",
            "symptoms_categories": [],
            "datetime": "",
        }
        for chunk in graph.stream(initial_state):
            for node_name, node_results in chunk.items():
                if node_name == "chatbot_agent":
                    chunk_answer = node_results.get("answer", [])
                    for message in chunk_answer:
                        # Update conversation history with chatbot response
                        initial_state["answer"] += message
                        yield message
                elif node_name == "logging_agent":
                    # Handle logging_agent output if needed
                    pass
                elif node_name == "update_conversation_history":
                    # Handle update_conversation_history output if needed
                    pass

    return StreamingResponse(
        event_stream(user_request, location), media_type="text/event-stream"
    )


if __name__ == "__main__":
    uvicorn.run(app)
