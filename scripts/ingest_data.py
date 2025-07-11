import chromadb
import json
import glob
import os

# Find the flattened JSON file
try:
    # Look in the data directory relative to the script's location
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, '..', 'data')
    flat_file_pattern = os.path.join(data_dir, 'nyc_tax_code_flat_*.json')
    flat_files = glob.glob(flat_file_pattern)
    if not flat_files:
        print("Error: No flattened JSON file found. Please run flatten_json.py first.")
        exit()
    flat_file = flat_files[0]
    print(f"Found data file: {flat_file}")
except IndexError:
    print("Error: No flattened JSON file found. Please run flatten_json.py first.")
    exit()

# Load the flattened data
print("Loading documents from JSON file...")
with open(flat_file, 'r') as f:
    documents = json.load(f)
print(f"Loaded {len(documents)} documents.")

# Initialize ChromaDB client. It will store data in a local directory.
print("Initializing ChromaDB client...")
client = chromadb.PersistentClient(path=os.path.join(data_dir, "chroma_db"))


# Create or get the collection
collection_name = "nyc_tax_code"
print(f"Getting or creating ChromaDB collection: '{collection_name}'...")
collection = client.get_or_create_collection(
    name=collection_name,
    metadata={"hnsw:space": "cosine"} # Use cosine similarity
)
print("Collection ready.")

# Prepare data for ChromaDB
print("Preparing data for ChromaDB...")
# ids = [doc['uid'] for doc in documents]
contents = [doc['text'] for doc in documents]
# metadatas = [doc['metadata'] for doc in documents]

# Sanitize metadata
print("Sanitizing metadata...")
clean_metadatas = []
for doc in documents:
    metadata = doc['metadata']
    clean_metadata = {}
    for key, value in metadata.items():
        if isinstance(value, list):
            clean_metadata[key] = ", ".join(map(str, value))
        elif value is None:
            clean_metadata[key] = ""
        else:
            clean_metadata[key] = value
    clean_metadatas.append(clean_metadata)

metadatas = clean_metadatas
print("Metadata sanitized.")


# Create unique IDs to avoid DuplicateIDError
print("Creating unique IDs...")
ids = []
seen_uids = {}
for i, doc in enumerate(documents):
    uid = doc['uid']
    if uid in seen_uids:
        seen_uids[uid] += 1
        new_id = f"{uid}_{seen_uids[uid]}"
    else:
        seen_uids[uid] = 0
        new_id = uid
    ids.append(new_id)
print("Unique IDs created.")


# Ingest data into ChromaDB in batches
print("Ingesting data into ChromaDB... (This may take a while)")
# The sentence-transformers model will be downloaded automatically by chromadb

batch_size = 200
num_documents = len(documents)
for i in range(0, num_documents, batch_size):
    batch_ids = ids[i:i+batch_size]
    batch_documents = contents[i:i+batch_size]
    batch_metadatas = metadatas[i:i+batch_size]
    
    print(f"Ingesting documents from {i} to {i+len(batch_ids)-1}...")
    collection.add(
        documents=batch_documents,
        metadatas=batch_metadatas,
        ids=batch_ids
    )

print(f"Successfully ingested {len(documents)} documents into the '{collection_name}' collection.")
