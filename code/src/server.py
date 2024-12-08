from dotenv import load_dotenv

load_dotenv()

from graph import MedicalGraph

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


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
async def ask(user_request):
    def event_stream(user_request: str):
        initial_state = {
            "user_request": user_request,
            "rephrased_request": "",
            "source_knowledge_pairs": [],
            "aggregated_knowledge": "",
            "answer": "",
        }
        for chunk in graph.stream(initial_state):
            for node_name, node_results in chunk.items():
                if node_name != "chatbot_agent":
                    continue
                chunk_answer = node_results.get("answer", [])
                for message in chunk_answer:
                    yield message

    return StreamingResponse(event_stream(user_request), media_type="text/event-stream")


@app.post("/debug")
async def debug_ask(user_request: str):
    initial_state = {
        "user_request": user_request,
        "rephrased_request": "",
        "source_knowledge_pairs": [],
        "aggregated_knowledge": "",
        "answer": "",
    }
    return graph.invoke(initial_state)


if __name__ == "__main__":
    uvicorn.run(app)
