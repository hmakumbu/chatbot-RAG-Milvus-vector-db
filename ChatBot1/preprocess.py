from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter


def process_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " ", ""], chunk_size=400, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    return docs


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
