from dotenv import load_dotenv

load_dotenv()

from graph import MedicalGraph
from database import Database

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn, json

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


# Define request body model
class UserRequest(BaseModel):
    conversation_history: list[dict]
    location: Optional[str] = None
    conversation_id: str


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.post("/")
async def ask(user_request: UserRequest):
    def event_stream(user_request: UserRequest):
        initial_state = {
            "rephrased_request": "",
            "source_knowledge_pairs": [],
            "aggregated_knowledge": "",
            "followup_question": "",
            "answer": "",
            "conversation_id": user_request.conversation_id,
            "location": user_request.location,
            "conversation_history": user_request.conversation_history,
            "summary": "",
            "symptoms_categories": [],
            "datetime": "",
            "processing_state": []
        }
        for stream_chunk in graph.stream(initial_state, stream_mode=["updates", "messages"]):
            if stream_chunk[0] == "messages":  # Stream the follow-up question, final answer or "unrelated" message
                message_chunk, metadata = stream_chunk[1]
                node_name = metadata.get("langgraph_node", "")
                node_trigger = metadata.get("langgraph_triggers", [""])[0]
                chunk_answer = getattr(message_chunk, "content", "")
                if node_name == "chatbot_agent" and node_trigger == "aggregation_agent":
                    yield json.dumps({"final_answer": chunk_answer})
                elif node_name == "validation_agent" and metadata.get("ls_temperature") == 0.1:
                    yield json.dumps({"answer": chunk_answer})
            elif stream_chunk[0] == "updates":  # Stream the processing state
                for _, attributes in stream_chunk[1].items():
                    if attributes:
                        processing_state = attributes.get('processing_state', [])
                        if processing_state:
                            yield json.dumps({"processing_state": processing_state[0]})

    return StreamingResponse(event_stream(user_request), media_type="text/event-stream")


@app.post("/debug")
async def debug_ask(user_request: UserRequest):
    initial_state = {
        "rephrased_request": "",
        "source_knowledge_pairs": [],
        "aggregated_knowledge": "",
        "followup_question": "",
        "answer": "",
        "conversation_id": user_request.conversation_id,
        "location": user_request.location,
        "conversation_history": user_request.conversation_history,
        "summary": "",
        "symptoms_categories": [],
        "datetime": "",
        "processing_state": []
    }
    return graph.invoke(initial_state)


@app.get("/conversations")
async def conversations():
    return json.dumps(Database().get_conversations())


if __name__ == "__main__":
    uvicorn.run(app)
