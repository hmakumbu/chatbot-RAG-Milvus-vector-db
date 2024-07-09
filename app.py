import streamlit as st
from ChatBot1.chatbot import ChatBot
import os
from dotenv import load_dotenv

load_dotenv()
DATA_PATH = os.getenv("DATAPATH")

# Fonction principale de l'application
def main():

      # Initialisation de Streamlit
    st.set_page_config(page_title="DataBeez Platform", page_icon=":bee:", layout="wide")
    
    # Chargement du logo
    logo_path = os.path.join("/Users/datadeep/Documents/LLMs/Chatbot Databeez/data/", "LogoDataBeez.jpg")
    

    st.markdown("<h1 style='text-align: center; color: white;'>Chat With DataBeez Platform LMS</h1>", unsafe_allow_html=True)
    
    # Sidebar de l'application
    with st.sidebar:
        st.title('DataBeez Platform LMS')
   
        st.image(logo_path, width=250)
    
    # Chargement des données et préparation de VectorDB
    file_path = os.path.join(DATA_PATH, "fake_document_calendrier_LMS.txt")
    
    file_path = os.path.join(DATA_PATH, "fake_document_calendrier_LMS.txt")
    
    # Initialisation du chatbot
    bot = ChatBot(file_path)

    # Stockage des messages générés par le LLM
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome to DataBeez Platform LMS"}]

    # Affichage des messages de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Entrée utilisateur avec une clé unique pour la réinitialisation
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0

    input_text = st.text_input("", key=f"input_{st.session_state.input_key}")

    if input_text:
        st.session_state.messages.append({"role": "user", "content": input_text})
        with st.chat_message("user"):
            st.write(input_text)

        # Génération d'une nouvelle réponse si le dernier message n'est pas de l'assistant
        if st.session_state.messages[-1]["role"] == "user":
            with st.chat_message("assistant"):
                with st.spinner("..."):
                    response = bot.chat(input_text)
                    st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)

        # Incrementer la clé pour réinitialiser le champ de texte
        st.session_state.input_key += 1
        st.experimental_rerun()

# Appel de la fonction principale pour exécuter l'application
if __name__ == "__main__":
    main()

