import streamlit as st
from ChatBot1.chatbot import ChatBot
#from ChatBot1.load import load
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
DATAPATH = os.getenv("DATAPATH")
FOLDER_PATH = os.getenv("FOLDER_PATH")
LOGO_PATH = os.path.join(DATAPATH, "aims-logo.png")
UPLOAD_DIRECTORY = os.path.join(FOLDER_PATH, "tempDir")

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.name)
    
    # Vérifier si le fichier existe déjà et écraser s'il existe
    # if os.path.exists(file_path):
    #     st.warning(f"Le fichier {uploaded_file.name} existe déjà. Il sera écrasé.")
    
    # with open(file_path, "wb") as f:
    #     f.write(uploaded_file.getbuffer())
    
    # return file_path

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.name)
     # Overwrite existing file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    st.set_page_config(page_title="DataBeez Platform", page_icon=":bee:", layout="wide")
    
    st.markdown("<h1 style='text-align: center; color: white;'>Chat with AMMI program</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.title('About AMMI Program')
        st.image(LOGO_PATH, width=250)

        uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx"])
    
    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file)

        bot = ChatBot(file_path)

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Welcome to AMMI program"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if "input_key" not in st.session_state:
            st.session_state.input_key = 0

        input_text = st.text_input("", key=f"input_{st.session_state.input_key}")

        if input_text:
            st.session_state.messages.append({"role": "user", "content": input_text})
            with st.chat_message("user"):
                st.write(input_text)

            if st.session_state.messages[-1]["role"] == "user":
                with st.spinner(""):
                    response = bot.chat(input_text)
                    st.write(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)

            st.session_state.input_key += 1
            st.experimental_rerun()

if __name__ == "__main__":
    main()


















# import streamlit as st
# from ChatBot1.chatbot import ChatBot
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DATAPATH = os.getenv("DATAPATH")
# LOGO_PATH = os.path.join(DATAPATH, "aims-logo.png")

# # Créer le dossier data s'il n'existe pas
# os.makedirs(DATAPATH, exist_ok=True)

# def main():
#     st.set_page_config(page_title="DataBeez Platform", page_icon=":bee:", layout="wide")
    
#     st.markdown("<h1 style='text-align: center; color: white;'>Chat with AMMI program</h1>", unsafe_allow_html=True)
    
#     with st.sidebar:
#         st.title('About AMMI Programm')
#         st.image(LOGO_PATH, width=250)

#         uploaded_file = st.file_uploader("Uploader un document", type=["txt"])
    
#     if uploaded_file:
#         file_path = os.path.join("/tmp", uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         bot = ChatBot(file_path)

#         if "messages" not in st.session_state:
#             st.session_state.messages = [{"role": "assistant", "content": "Welcome to AMMI programm"}]

#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.write(message["content"])

#         if "input_key" not in st.session_state:
#             st.session_state.input_key = 0

#         input_text = st.text_input("", key=f"input_{st.session_state.input_key}")

#         if input_text:
#             st.session_state.messages.append({"role": "user", "content": input_text})
#             with st.chat_message("user"):
#                 st.write(input_text)

#             if st.session_state.messages[-1]["role"] == "user":
#                 with st.chat_message("assistant"):
#                     with st.spinner(""):
#                         response = bot.chat(input_text)
#                         st.write(response)
#                 message = {"role": "assistant", "content": response}
#                 st.session_state.messages.append(message)

#             st.session_state.input_key += 1
#             st.experimental_rerun()

# if __name__ == "__main__":
#     main()
