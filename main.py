from fastapi import FastAPI, UploadFile, File, Form
from app.services.pdf_service import PDF_Service
from app.services.queryService import Query_Service
app = FastAPI()
mdFile = PDF_Service.convertFileToMD("./assets/receitas.pdf")
chuncks = PDF_Service.covertMDToChunks(mdFile)
embed = PDF_Service.embed(chuncks)
result = Query_Service.query(embed, "Quais são os ingredientes do bife de marinheiro?")

# @app.post("/upload")
# async def upload_endpoint(
#     file: UploadFile = File(...),
#     query: str = Form(...)
# ):  return "a"


# print(result.document.export_to_markdown())