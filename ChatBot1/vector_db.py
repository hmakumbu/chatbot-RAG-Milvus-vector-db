from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()
milvus_host = os.getenv("MILVUS_HOST", "localhost")
milvus_port = int(os.getenv("MILVUS_PORT", 19530))
connections.connect("default", host=milvus_host, port=milvus_port)

# Check the model output dimension
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
dimension = 384

def vector_db(docs, collection_name="demo"):
    # Drop the collection if it exists
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension)
    ]

    schema = CollectionSchema(fields=fields, enable_dynamic_field=True)
    demo = Collection(collection_name, schema=schema)

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",
        "params": {"nlist": 128}
    }

    demo.create_index(
        field_name="vector",
        index_params=index_params
    )

    ids = []
    vectors = []
    for i, doc in enumerate(docs):
        embeddings = model.encode(doc.page_content)
        vector = embeddings.tolist()
        ids.append(i)
        vectors.append(vector)

    # Insert the data as separate lists for each field
    demo.insert([ids, vectors])

     # Load the collection into memory
    demo.load()

    # Return a callable retriever
    def retriever(query):
        if isinstance(query, dict) and 'question' in query:
            query = query['question']
        elif not isinstance(query, str):
            raise ValueError(f"Unexpected query format: {query}")

        # Encode the query and perform a search on the collection
        query_embedding = model.encode(query).tolist()
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
        results = demo.search([query_embedding], "vector", param=search_params, limit=10)
        return results

    return retriever
