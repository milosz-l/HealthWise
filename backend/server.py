from dotenv import load_dotenv

load_dotenv()

from graph import MedicalGraph

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional

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
    user_request: str
    location: Optional[str] = None
    conversation_id: str


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.post("/")
async def ask(user_request: UserRequest):
    def event_stream(user_request: UserRequest):
        initial_state = {
            "user_request": user_request.user_request,
            "rephrased_request": "",
            "source_knowledge_pairs": [],
            "aggregated_knowledge": "",
            "answer": "",
            "conversation_id": user_request.conversation_id,
            "location": user_request.location,
            "conversation_history": [{"user": user_request.user_request}],
            "summary": "",
            "symptoms_categories": [],
            "datetime": "",
        }
        for chunk in graph.stream(initial_state, stream_mode="messages"):
            message_chunk, metadata = chunk
            node_name = metadata.get("langgraph_node", "")
            node_trigger = metadata.get("langgraph_triggers", [""])[0]
            if node_name == "chatbot_agent" and node_trigger == "aggregation_agent":
                chunk_answer = getattr(message_chunk, "content", "")
                yield chunk_answer

    return StreamingResponse(event_stream(user_request), media_type="text/event-stream")


@app.post("/debug")
async def debug_ask(user_request: UserRequest):
    initial_state = {
        "user_request": user_request.user_request,
        "rephrased_request": "",
        "source_knowledge_pairs": [],
        "aggregated_knowledge": "",
        "answer": "",
        "conversation_id": user_request.conversation_id,
        "location": user_request.location,
        "conversation_history": [{"user": user_request.user_request}],
        "summary": "",
        "symptoms_categories": [],
        "datetime": "",
    }
    return graph.invoke(initial_state)


if __name__ == "__main__":
    uvicorn.run(app)
