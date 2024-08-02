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
dimension = model.get_sentence_embedding_dimension()

def vector_db(docs, collection_name="demo"):
    # Drop the collection if it exists
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=500)  # Adding content field for storage
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
    contents = []
    for i, doc in enumerate(docs):
        if isinstance(doc, str):
            text_content = doc  # Directly use the document content if it's already a string
        else:
            text_content = doc.page_content  # Assuming doc has a 'page_content' attribute or similar
        
        embeddings = model.encode(text_content)
        vector = embeddings.tolist()
        ids.append(i)
        vectors.append(vector)
        contents.append(text_content)  # Store the document content
       # print(f"Document {i}: {text_content}")
       # print(f"Vector: {vector[:5]}...")  # Print first 5 dimensions for brevity

    # Insert the data as separate lists for each field
    demo.insert([ids, vectors, contents])

    # Load the collection into memory
    demo.load()

    # Verify inserted data
    results = demo.query(expr="id >= 0", output_fields=["id", "content"])
    #print("Stored vectors:", results)

    # Return a callable retriever
    def retriever(query):
        if isinstance(query, dict) and 'question' in query:
            query = query['question']
        elif not isinstance(query, str):
            raise ValueError(f"Unexpected query format: {query}")

        # Encode the query and perform a search on the collection
        query_embedding = model.encode(query).tolist()
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
        results = demo.search([query_embedding], "vector", param=search_params, limit=10, output_fields=["id", "content"])
        
        # Check search results
        #print("Search results:", results)
        
        # Fetch detailed content of the results
        search_results = []
        if results:
            for result in results[0]:
                entity = demo.query(expr=f"id == {result.id}", output_fields=["id", "content"])
                if entity:
                    search_results.append(entity[0]['content'])
                #print(f"Entity for id {result.id}:", entity)

        return search_results

    return retriever


# from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility
# from sentence_transformers import SentenceTransformer
# from dotenv import load_dotenv
# import os

# load_dotenv()
# milvus_host = os.getenv("MILVUS_HOST", "localhost")
# milvus_port = int(os.getenv("MILVUS_PORT", 19530))
# connections.connect("default", host=milvus_host, port=milvus_port)

# # Check the model output dimension
# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# dimension = model.get_sentence_embedding_dimension()

# def vector_db(docs, collection_name="demo"):
#     # Drop the collection if it exists
#     if utility.has_collection(collection_name):
#         utility.drop_collection(collection_name)

#     fields = [
#         FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
#         FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
#         FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=500)  # Adding content field for storage
#     ]

#     schema = CollectionSchema(fields=fields, enable_dynamic_field=True)
#     demo = Collection(collection_name, schema=schema)

#     index_params = {
#         "index_type": "IVF_FLAT",
#         "metric_type": "COSINE",
#         "params": {"nlist": 128}
#     }

#     demo.create_index(
#         field_name="vector",
#         index_params=index_params
#     )

#     ids = []
#     vectors = []
#     contents = []
#     for i, doc in enumerate(docs):
#         embeddings = model.encode(doc.page_content)
#         vector = embeddings.tolist()
#         ids.append(i)
#         vectors.append(vector)
#         contents.append(doc.page_content)  # Store the document content
#         print(f"Document {i}: {doc.page_content}")
#         print(f"Vector: {vector[:5]}...")  # Print first 5 dimensions for brevity

#     # Insert the data as separate lists for each field
#     demo.insert([ids, vectors, contents])

#     # Load the collection into memory
#     demo.load()

#     # Verify inserted data
#     results = demo.query(expr="id >= 0", output_fields=["id", "content"])
#     print("Stored vectors:", results)

#     # Return a callable retriever
#     def retriever(query):
#         if isinstance(query, dict) and 'question' in query:
#             query = query['question']
#         elif not isinstance(query, str):
#             raise ValueError(f"Unexpected query format: {query}")

#         # Encode the query and perform a search on the collection
#         query_embedding = model.encode(query).tolist()
#         search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
#         results = demo.search([query_embedding], "vector", param=search_params, limit=10, output_fields=["id", "content"])
        
#         # Check search results
#         print("Search results:", results)
        
#         # Fetch detailed content of the results
#         search_results = []
#         if results:
#             for result in results[0]:
#                 entity = demo.query(expr=f"id == {result.id}", output_fields=["id", "content"])
#                 if entity:
#                     search_results.append(entity[0]['content'])
#                 print(f"Entity for id {result.id}:", entity)

#         return search_results

#     return retriever
