from fastapi import FastAPI, UploadFile, File, Form
from app.services.pdf_service import PDFService

app = FastAPI()
mdFile = PDFService.convertFileToMD("./assets/receitas.pdf")
chuncks = PDFService.covertMDToChunks(mdFile)
print(chuncks)

# @app.post("/upload")
# async def upload_endpoint(
#     file: UploadFile = File(...),
#     query: str = Form(...)
# ):  return "a"


# print(result.document.export_to_markdown())