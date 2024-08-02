from ChatBot1.load import load
from ChatBot1.vector_db import vector_db
from ChatBot1.preprocess import process_documents


def get_retriever(file_path):

    # Chargement des données textuelles
    data = load(file_path)
    
    # Prétraitement des documents
    docs = process_documents(data)
    
    # Création de l'instance VectorDB avec le nom de collection approprié
    retriever = vector_db(docs=docs)
        
    return  retriever