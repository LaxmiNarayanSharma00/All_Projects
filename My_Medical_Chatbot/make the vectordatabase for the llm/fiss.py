import pandas as pd
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from tqdm import tqdm  
import faiss  
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable in a .env file or your environment.")

# Load your dataset
file_path = '/home/dreambig/Downloads/remote job/ai-medical-chatbot-master/8-Interviewer/dialogues_embededd.pkl'
data = pd.read_pickle(file_path)
texts = data['combined'].tolist()

# Initialize embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_api_key)

# Convert texts to Document objects
print("Converting texts to Document objects...")
documents = [Document(page_content=text) for text in texts]

# Generate embeddings with progress bar
print("Generating embeddings...")
embeddings = []
for doc in tqdm(documents, desc="Embedding texts", unit="docs"):
    embeddings.append(embedding_model.embed_documents([doc.page_content])[0])

embeddings = np.array(embeddings, dtype=np.float32)

# Save embeddings before proceeding further
os.makedirs('knowledge', exist_ok=True)
np.save('knowledge/embeddings.npy', embeddings)
print("Embeddings saved successfully at 'knowledge/embeddings.npy'.")

# Create FAISS index
print("Creating FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Prepare docstore and index mapping
from langchain.docstore import InMemoryDocstore

docstore = InMemoryDocstore({i: doc for i, doc in enumerate(documents)})
index_to_docstore_id = {i: i for i in range(len(documents))}

# Create FAISS vector store
faiss_vectorstore = FAISS(
    embedding_function=embedding_model,
    index=index,
    docstore=docstore,
    index_to_docstore_id=index_to_docstore_id
)

# Save the index locally
faiss_vectorstore.save_local("knowledge/faiss_index_all_documents")

print("FAISS index created and saved successfully at 'knowledge/faiss_index_all_documents'.")
