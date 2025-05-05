import re
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class CustomStrOutputParser(StrOutputParser):
    def __init__(self) -> None:
        super().__init__()

    def extract_answer(self, text_respone: str,
                       partent: str = r"Answer:\s*(.*)") -> str:

        match = re.search(partent, text_respone, re.DOTALL)
        if match:
            answer_text = match.group(1).strip()
            return answer_text
        else:
            text_respone

    def parse(self, text: str):
        return self.extract_answer(text)


class OfflineRag:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = hub.pull("rlm/rag-prompt")
        self.str_parser = CustomStrOutputParser()

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_chain(self, retriever):
        input_data = {
            "context": retriever | self.format_docs,
            "question": RunnablePassthrough()
        }

        rag_chain = (input_data
                     | self.prompt
                     | self.llm
                     | self.str_parser
                    )
        return rag_chain
