from dotenv import load_dotenv
load_dotenv()

from graph import MedicalGraph

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
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
    initial_state = {
        "user_request": user_request,
        "rephrased_request": "",
        "source_knowledge_pairs": [],
        "aggregated_knowledge": "",
        "answer": ""
    }
    response = await graph.ainvoke(input=initial_state)
    return response

if __name__ == "__main__":
    uvicorn.run(app)