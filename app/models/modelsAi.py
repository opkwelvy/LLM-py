import os
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_openai import AzureChatOpenAI

gpt4o = AzureChatOpenAI(
     azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_API_INSTANCE_NAME')}.openai.azure.com",
    openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
    azure_deployment=os.getenv('AZURE_OPENAI_API_DEPLOYMENT_NAME'),
    openai_api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    model_name="gpt-4o",
    temperature=0
)
embeddings = OllamaEmbeddings(
    model=os.getenv('OLLAMA_MODEL'),
    base_url=os.getenv('OLLAMA_BASE_URL'),
)