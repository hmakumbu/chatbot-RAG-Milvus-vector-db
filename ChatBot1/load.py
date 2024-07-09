
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv

load_dotenv()

def load_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    loader = TextLoader(file_path)
    documents = loader.load()

    return documents


