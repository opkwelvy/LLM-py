from fastapi import FastAPI, UploadFile, File, Form
from app.services.pdf_service import PDF_Service
from app.services.queryService import Query_Service
from dotenv import load_dotenv
import asyncio
load_dotenv()

async def main():
    mdFile = PDF_Service.convertFileToMd("./assets/receitas.pdf")
    chunks =  PDF_Service.mdFileToChunks(mdFile)
    embed =  PDF_Service.embed(chunks)
    
    result = await Query_Service.query(embed, "Quais são os ingredientes do bife de marinheiro?")
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

