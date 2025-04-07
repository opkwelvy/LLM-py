import os
import re
import tempfile
from docling.document_converter import DocumentConverter 
from ..utils.utils import UtilsText
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from langchain_community.document_loaders import PyPDFLoader
from ..models.modelsAi import embeddings
class PDF_Service:
    @staticmethod
    def convertFile(file_path:str) -> str:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        return docs
        
    @staticmethod
    def convertFileToMd(file_path:str)-> str:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        return result.document.export_to_markdown()
    
    @staticmethod
    def mdFileToChunks(markdown_content: str) -> list[str]:   
        cleaned_content = re.sub(r'(<!-- image -->\s*){2,}', '<!-- image -->\n', markdown_content)
        chunks = UtilsText.chunck_PDF(cleaned_content)  # Agora passando caminho do arquivo
        recipe_chunks = []
        current_recipe = []
    
        for chunk in chunks:
            content = chunk.page_content
            if "## \\_ Ingredientes" in content or "## \\_ Modo de preparo" in content:
                if current_recipe:  # Se já temos uma receita acumulada
                    recipe_chunks.append("\n".join(current_recipe))
                    current_recipe = []
                current_recipe.append(content)
            else:
                current_recipe.append(content)
    
        if current_recipe:  # Adiciona a última receita
            recipe_chunks.append("\n".join(current_recipe))
            return [doc.page_content for doc in chunks]
        
    @staticmethod
    def createChunks(mdFile:str) -> list[str]:
        contents = [doc.page_content for doc in mdFile]
        return contents
    @staticmethod
    def embed(content:list[str])-> VectorStore:
        vector_store = InMemoryVectorStore.from_texts(content, embeddings)
        return vector_store