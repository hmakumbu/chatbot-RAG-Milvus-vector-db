from langchain_community.chat_models import ChatOllama
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialiser le modèle LLM
local_model = "mistral"
llm = ChatOllama(model=local_model)