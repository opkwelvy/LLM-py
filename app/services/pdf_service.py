
# from docling.document_converter import DocumentConverter 
from ..utils.utils import UtilsText
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from langchain_community.document_loaders import PyPDFLoader
from ..models.modelsAi import embeddings
class PDF_Service:
    @staticmethod
    def convertFileToMD(file_path:str) -> str:
        print("convertFileToMD")
        # converter = DocumentConverter()
        print("antes")
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        # result = converter.convert(filePath)
        print("depois")
        return docs
        # return result.document.export_to_markdown
    @staticmethod
    def covertMDToChunks(mdFile:str) -> list[str]:
        print("covertMDToChunks")
        # chuncks = UtilsText.chunck_PDF(mdFile)
        contents = [doc.page_content for doc in mdFile]
        return contents
    @staticmethod
    def embed(content:list[str])-> VectorStore:
        print("embed")
        vector_store = InMemoryVectorStore.from_texts(content, embeddings)
        return vector_store