# Chatbot RAG with Milvus and Streamlit

## Description
This project aims to create a chatbot using the Retrieval-Augmented Generation (RAG) technique. The chatbot utilizes the Milvus vector database for storage and information retrieval and is deployed with a Streamlit interface.

## Prerequisites
- Python 3.8+
- Poetry for dependency management

## Installation
Clone the repository and install dependencies using Poetry:

```bash
git clone <your-repository>
cd <your-repository>
poetry install
```

## Configuration
Make sure to create a `.env` file containing the necessary environment variables.

## Running the Application
Navigate to the directory containing `app.py` and run the application with the following command:

```bash
streamlit run app.py
```

## Features
- **Document Loading**: Load PDF files using `PdfReader`.
- **Preprocessing**: Documents are split into manageable sections with `RecursiveCharacterTextSplitter`.
- **Vector Database**: Milvus is used to store and retrieve document vectors.
- **Response Generation**: Language models are used to generate responses based on retrieved documents.
- **User Interface**: Streamlit provides a simple and interactive web interface.
