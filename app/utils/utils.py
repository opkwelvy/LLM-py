from langchain_community.document_loaders import TextLoader
class UtilsText:
    @staticmethod
    def chunck_PDF(mdFile:str)-> list:
        loader = TextLoader(mdFile, encoding="utf-8")
        docs = loader.load()
        return docs