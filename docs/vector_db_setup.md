# Vector Database Setup for NYC Tax Code

This document outlines the process of setting up a vector database to ingest and search the flattened NYC tax code data. This is a crucial step towards building a Retrieval-Augmented Generation (RAG) system.

We will use `chromadb` as our vector database. It's a lightweight, open-source vector database that's easy to set up and use for local development. We will also use `sentence-transformers` to generate vector embeddings for our text data.

## Plan

1.  **Update Dependencies**: Add `chromadb` and `sentence-transformers` to our `requirements.txt` file.

2.  **Ingest Data**: Create a new script `scripts/ingest_data.py` that will:
    *   Read the flattened JSON data from `data/nyc_tax_code_flat_*.json`.
    *   Generate vector embeddings for each text entry using a pre-trained model from `sentence-transformers`.
    *   Initialize a `chromadb` client and create a collection.
    *   Store the text, metadata, and embeddings in the `chromadb` collection.

3.  **Search Data**: Create a new script `scripts/search_data.py` that will:
    *   Take a text query from the command line.
    *   Generate an embedding for the query.
    *   Query the `chromadb` collection to find the most relevant documents based on semantic similarity.
    *   Print the search results.

This setup will allow us to perform semantic searches over the entire NYC tax code.
