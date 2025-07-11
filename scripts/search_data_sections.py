import chromadb
import argparse
import os

# Setup argument parser
parser = argparse.ArgumentParser(description="Search the NYC tax code using section-level documents.")
parser.add_argument("query", type=str, help="The search query.")
parser.add_argument("-n", "--num_results", type=int, default=5, help="Number of results to return.")
args = parser.parse_args()

# Initialize ChromaDB client
script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')
client = chromadb.PersistentClient(path=os.path.join(data_dir, "chroma_db"))

# Get the section-level collection
collection_name = "nyc_tax_code_sections"
try:
    collection = client.get_collection(name=collection_name)
except Exception as e:
    print(f"Error: Could not find collection '{collection_name}'. Please run ingest_data_sections.py first.")
    print(f"Error details: {e}")
    exit()

# Query the collection
print(f"Searching section-level documents for: '{args.query}'...")
results = collection.query(
    query_texts=[args.query],
    n_results=args.num_results
)

# Print the results
print(f"Found {len(results['ids'][0])} section-level results for '{args.query}':\n")
for i, doc_id in enumerate(results['ids'][0]):
    distance = results['distances'][0][i]
    metadata = results['metadatas'][0][i]
    document = results['documents'][0][i]
    
    print(f"Result {i+1} (ID: {doc_id}, Distance: {distance:.4f}):")
    print(f"  Section: {metadata.get('full_citation', 'N/A')} - {metadata.get('section_name', 'N/A')}")
    print(f"  Path: {metadata.get('title', 'N/A')} > Chapter {metadata.get('chapter_number', 'N/A')}: {metadata.get('chapter_title', 'N/A')}")
    print(f"  Has Subsections: {metadata.get('has_subsections', 'N/A')} (Total: {metadata.get('total_subsections', 'N/A')})")
    print(f"  Text Length: {len(document)} characters")
    
    # Show first 500 characters of text for readability
    if len(document) > 500:
        print(f"  Text Preview: {document}")
    else:
        print(f"  Text: {document}")
    
    print("-" * 80)

print(f"\nNote: Results are from section-level documents containing complete sections with all subsections.")
