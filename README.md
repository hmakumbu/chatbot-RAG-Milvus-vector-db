# Chatbot RAG with Milvus and Streamlit

## Description
This project aims to create a AI chatbot with LangChain using the Retrieval-Augmented Generation (RAG) technique. The chatbot utilizes the Milvus vector database for storage and information retrieval and is deployed with a Streamlit interface. You can upload your own data to particulazise this AI ChatBot.

For my personal case, I used the data of African Master's in Machine Intelligence (AMMI). In This case, the chatbot is designed to assist students in navigating AMMI program by providing relevant information about courses, scholarships, schedules, opportunities, code of conduct and more. The chatbot also offers guidance on academic orientations. 

The impact of this project has been significant. It has streamlined the process for students to access vital information, reducing the workload on administrative staff and improving the overall user experience on our platform. The chatbot’s ability to provide personalized advice and timely information has enhanced student engagement and satisfaction.

## Prerequisites
- Python 3.8+
- Poetry for dependency management

## Installation
Clone the repository and install requirement.txt:

```bash
pip install requirement.txt
```

For Docker and Milvus installation, refer to this [link](https://milvus.io/docs/install_standalone-docker.md)

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
