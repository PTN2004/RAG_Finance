from pydantic import BaseModel, Field

from src.rag.file_loader import Loader
from src.rag.vectorstore import VectorDatabase
from src.rag.offline_rag import OfflineRag

class InputQA(BaseModel):
    question:str = Field(..., title="Question to ask the model")

class OutputQA(BaseModel):
    answer:str = Field(..., title= "Answer from the model")

def build_rag_chain(llm, data_dir, data_type):
    doc_loader = Loader(data_type).load_dir(data_dir, workers=2)
    retriever = VectorDatabase(doc_loader).get_retriever()
    rag_chain = OfflineRag(llm).get_chain(retriever=retriever)
    return rag_chain