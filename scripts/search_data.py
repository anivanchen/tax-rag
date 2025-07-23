import chromadb
import argparse
import os
from keybert import KeyBERT

# Initialize KeyBERT model
kw_model = KeyBERT()

# Setup argument parser
parser = argparse.ArgumentParser(description="Search the NYC tax code.")
parser.add_argument("query", type=str, help="The search query.")
parser.add_argument("-n", "--num_results", type=int, default=5, help="Number of results to return.")
args = parser.parse_args()

# --- Query Expansion ---
# Extract keywords from the query to create a richer search query
print("Extracting keywords from query to augment search...")
try:
    query_keywords_tuples = kw_model.extract_keywords(args.query, 
                                                    keyphrase_ngram_range=(1, 2), 
                                                    stop_words='english')
    query_keywords = [kw[0] for kw in query_keywords_tuples]
    
    if query_keywords:
        search_query = " ".join(query_keywords)
        print(f"Using extracted keywords for search: {search_query}\n")
    else:
        print("No keywords extracted, using original query.\n")
        search_query = args.query

except Exception as e:
    print(f"Could not generate keywords for query. Using original query. Error: {e}")
    search_query = args.query
# -----------------------

# Initialize ChromaDB client
script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')
client = chromadb.PersistentClient(path=os.path.join(data_dir, "chroma_db"))

# Get the collection
collection_name = "nyc_tax_code_keyworded"
collection = client.get_collection(name=collection_name)

# Query the collection
results = collection.query(
    query_texts=[search_query],
    n_results=args.num_results
)

# Print the results
print(f"Found {len(results['ids'][0])} results for '{args.query}':\n")
for i, doc_id in enumerate(results['ids'][0]):
    distance = results['distances'][0][i]
    metadata = results['metadatas'][0][i]
    document = results['documents'][0][i]
    
    print(f"Result {i+1} (ID: {doc_id}, Distance: {distance:.4f}):")
    print(f"  Path: {metadata.get('title', 'N/A')} > {metadata.get('chapter_title', 'N/A')} > {metadata.get('section_name', 'N/A')}")
    print(f"  Text: {document}") # Print full text
    print("-" * 20)
