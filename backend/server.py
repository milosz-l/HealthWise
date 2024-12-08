from dotenv import load_dotenv

load_dotenv()

from graph import MedicalGraph

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid

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
        conversation_id = str(uuid.uuid4())  # TODO: move it to frontend
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
        for chunk in graph.stream(initial_state, stream_mode="messages"):
            message_chunk, metadata = chunk
            node_name = metadata.get('langgraph_node', '')
            node_trigger = metadata.get('langgraph_triggers', '')[0]
            if node_name == "chatbot_agent" and node_trigger == "aggregation_agent":
                chunk_answer = getattr(message_chunk, 'content', '')
                yield chunk_answer

    return StreamingResponse(
        event_stream(user_request, location), media_type="text/event-stream"
    )


@app.post("/debug")
async def debug_ask(user_request: str, location: str):
    conversation_id = str(uuid.uuid4())  # TODO: move it to frontend
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
    return graph.invoke(initial_state)


if __name__ == "__main__":
    uvicorn.run(app)
