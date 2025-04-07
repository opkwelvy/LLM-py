from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownTextSplitter
class UtilsText:
    @staticmethod
    def chunck_PDF(mdFile:str)-> list:
       
        splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        return splitter.create_documents([mdFile])
