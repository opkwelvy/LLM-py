import os
import re
import tempfile
import fitz
from PIL import Image
import io
import base64
from docling.document_converter import DocumentConverter 
from transformers import BlipProcessor, BlipForConditionalGeneration
from ..utils.utils import UtilsText
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from langchain_community.document_loaders import PyPDFLoader
from ..models.modelsAi import embeddings
class PDF_Service:
    @staticmethod
    def extract_images_and_descriptions(file_path: str) -> list[str]:
        doc = fitz.open(file_path)
        image_descriptions = []

        for i, page in enumerate(doc):
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                img_pil = Image.open(io.BytesIO(image_bytes))

                # Converta imagem para base64 para facilitar o transporte (opcional)
                if img_pil.mode == "CMYK":
                    img_pil = img_pil.convert("RGB")
                buffered = io.BytesIO()
                img_pil.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

                # Gerar descrição da imagem via IA (aqui está um placeholder)
                description = PDF_Service.describe_image_with_ai(img_pil)

                image_descriptions.append(f"iDescrição da imagem: {description}")

        return image_descriptions
    
    @staticmethod
    def describe_image_with_ai(image_pil: Image.Image) -> str:
        import torch
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        inputs = processor(images=image_pil, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    
    @staticmethod
    def convertFile(file_path:str) -> str:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        return docs
        
    @staticmethod
    def convertFileToMd(file_path:str)-> str:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        markdown = result.document.export_to_markdown()
        image_descriptions = PDF_Service.extract_images_and_descriptions(file_path)
        for description in image_descriptions:
            if "<!-- image -->" in markdown:
                markdown = markdown.replace("<!-- image -->", description, 1)
                
        return markdown
    
    @staticmethod
    def mdFileToChunks(markdown_content: str) -> list[str]:   
        cleaned_content = re.sub(r'(<!-- image -->\s*){2,}', '<!-- image -->\n', markdown_content)
        chunks = UtilsText.chunck_PDF(cleaned_content) 
        recipe_chunks = []
        current_recipe = []
    
        for chunk in chunks:
            content = chunk.page_content
            if "## \\_ Ingredientes" in content or "## \\_ Modo de preparo" in content:
                if current_recipe: 
                    recipe_chunks.append("\n".join(current_recipe))
                    current_recipe = []
                current_recipe.append(content)
            else:
                current_recipe.append(content)
    
        if current_recipe: 
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