
from docling.document_converter import DocumentConverter
from ..utils.utils import UtilsText
class PDFService:
    @staticmethod
    def convertFileToMD(filePath:str) -> str:
        converter = DocumentConverter()
        result = converter.convert(filePath)
        return result.document.export_to_markdown
    @staticmethod
    def covertMDToChunks(mdFile:str) -> list[str]:
        chuncks = UtilsText.chunck_PDF(mdFile)
        return chuncks