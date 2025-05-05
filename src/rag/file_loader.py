import glob
import multiprocessing
import multiprocessing.util

from tqdm import tqdm
from typing import Union, Literal, List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def remove_no_utf8(text):
    return "".join(char for char in text if ord(char) < 128)


def load_documents(file_path):
    docs = PyPDFLoader(file_path=file_path, extract_images=True).load()

    for doc in docs:
        doc.page_content = remove_no_utf8(doc.page_content)
    return docs


def get_num_cpu():
    return multiprocessing.cpu_count()


class BaseLoader():
    def __init__(self) -> None:
        self.num_processing = get_num_cpu()

    def __call__(self, files: List[str], **kwargs):
        pass


class PDFLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, pdf_files: List[str], **kwargs):
        
        doc_loaded = []
        total_file = len(pdf_files)
        with tqdm(total=total_file, desc="Loading PDFs", unit="file") as pbar:
            for file_path in pdf_files:
                print(file_path)
                result = load_documents(file_path=file_path)
                doc_loaded.extend(result)
                pbar.update(1)

        return doc_loaded


class TextSplitter:
    def __init__(
            self, separators: List[str] = ['\n\n', '\n', ' ', ''],
            chunk_size: int = 300,
            chunk_overlap: int = 0
    ) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_overlap=chunk_overlap,
            chunk_size=chunk_size

        )

    def __call__(self, documents):
        return self.splitter.split_documents(documents)


class Loader:
    def __init__(self,
                 file_type: Literal['pdf'],
                 splitter_kwagrs: dict = {
                     "chunk_size": 300,
                     "chunk_overlap": 0}
                 ):
        assert file_type in ["pdf"], "file must pdf"
        self.file_type = file_type
        if file_type == "pdf":
            self.doc_loader = PDFLoader()
        else:
            raise ValueError("File must pdf ")

        self.splitter = TextSplitter(**splitter_kwagrs)

    def load(self, pdf_files: Union[str, List[str]], workers: int = 1):
        if isinstance(pdf_files, str):
            pdf_files = [pdf_files]

        doc_loaded = self.doc_loader(pdf_files, workers=workers)
        doc_splitted = self.splitter(doc_loaded)

        return doc_splitted

    def load_dir(self, dir_path: int, workers: int = 1):
        if self.file_type == "pdf":
            files = glob.glob(f"{dir_path}/*.pdf")
            assert len(
                files) > 0, f"No {self.file_type} file not found in {dir_path}"
        else:
            raise ValueError("File must pdf")

        return self.load(files)
