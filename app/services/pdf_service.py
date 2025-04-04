
from docling.document_converter import DocumentConverter
from ..utils.utils import UtilsText
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from ..models.modelsAi import embeddings
class PDF_Service:
    @staticmethod
    def convertFileToMD(filePath:str) -> str:
        converter = DocumentConverter()
        result = converter.convert(filePath)
        return result.document.export_to_markdown
    @staticmethod
    def covertMDToChunks(mdFile:str) -> list[str]:
        chuncks = UtilsText.chunck_PDF(mdFile)
        contents = [doc.page_content for doc in chuncks]
        return contents
    @staticmethod
    def embed(content:list[str])-> VectorStore:
        vector_store = InMemoryVectorStore.from_texts(content, embeddings)
        return vector_store