from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from ..models.modelsAi import gpt4o
class Query_Service:
    async def query(embed: VectorStore, user_input: str) :
        try:
            retriever = embed.as_retriever(k=3)
            prompt = PromptTemplate.from_template("""
            You are an LLM with one goal: to help the user answer questions about the following topic:
         {context}
         
Now, answer the following question: {input}                                   
                                                  """)
            
            document_chain = create_stuff_documents_chain(gpt4o, prompt)
            context = await retriever.ainvoke(user_input)
            result = await document_chain.ainvoke({
                "input":user_input,
                "context": context
            })
            return result
        except Exception as e:
            print(f"Error in query: {e}")
            raise