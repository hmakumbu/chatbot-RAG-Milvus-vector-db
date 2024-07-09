from langchain.document_loaders import TextLoader
from get_model_features import get_retriever
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from ChatBot1.prompt import prompt
from ChatBot1.setModel import llm
import os

class ChatBot:
    
    def __init__(self, file_path):
        # Get the document retriever from get_retriever
        self.retriever_callable = get_retriever(file_path)
        
        # Load the documents from the text file
        self.loader = TextLoader(file_path)
        self.documents = self.loader.load()

        # Configure the RAG (retrieval-augmented generation) chain
        self.rag_chain = (
            {"context": {"retriever": self.retriever_callable}, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def chat(self, question):
        # Call the RAG chain to generate a response from the question
        return self.rag_chain.invoke({"context": self.documents, "question": question})


