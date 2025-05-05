import os
os.environ['TOKENIZERS_PARALLELISM'] = "false"
print(os.getenv("LANGCHAIN_API_KEY"))

from langserve import add_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.base.llm_model import get_model
from src.rag.main import build_rag_chain, InputQA, OutputQA

llm = get_model()
data_dir = "./data_source"
rag_chain = build_rag_chain(llm, data_dir, "pdf")

app = FastAPI(
    title="Rag finance server",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]   
)

@app.get("/check")
async def check():
    return {"status" : "OK"}

@app.post("/generative_ai", response_model=OutputQA)
async def generative_ai(inputs:InputQA):
    answer = rag_chain.invoke(inputs.question)
    return {"answer": answer}

add_routes(
    app,
    rag_chain,
    playground_type="default",
    path="/generative_ai"
)