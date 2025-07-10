# NYC Legislative RAG + LLM System

## Project Overview

This project aims to build a robust Retrieval-Augmented Generation (RAG) system to manage and analyze the constantly evolving NYC Administrative Code, with a primary focus on the NYC Tax Code. While the initial focus is on the NYC code, the system is designed to incorporate other sources, such as New York State laws and other relevant legal and financial documents. The system's core functionality is to ingest new legislative documents, automatically identify their impact on existing law, track all historical versions of legal provisions, and generate structured summaries of changes for economic analysis.

This repository contains the initial data processing pipeline for this system.

## Current Progress & Key Scripts

The initial data processing pipeline is complete. It parses the raw NYC Administrative Code and transforms it into a format suitable for a vector database and a RAG system.

1.  **`parse_code.py`**:
    *   **Purpose**: Parses the source `nyc-tax-code.html` file.
    *   **Output**: Creates `nyc_tax_code.json`, a hierarchical JSON representation of the legal code.
    *   **Documentation**: See [`parse_docs.md`](./parse_docs.md) for details.

2.  **`flatten_json.py`**:
    *   **Purpose**: Ingests the hierarchical `nyc_tax_code.json` and flattens it. Each granular section of the code becomes a separate JSON object, enriched with extensive metadata for versioning, context, and future analysis.
    *   **Output**: Creates `nyc_tax_code_flat_20250710.json`.
    *   **Documentation**: See [`flatten_docs.md`](./flatten_docs.md) for details.

The resulting flattened JSON is now ready for the next stage: embedding and ingestion into a vector database.

## Setup and Usage

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv env
    ```

2.  **Activate the virtual environment:**
    ```bash
    source env/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the data processing pipeline:**
    ```bash
    # Step 1: Parse the source HTML into hierarchical JSON
    python3 parse_code.py

    # Step 2: Flatten the JSON and add metadata
    python3 flatten_json.py
    ```

## Next Steps

Based on the project plan outlined in `PLANS.md`, the next steps involve:

1.  **Vector Database Setup**: Setting up an Elasticsearch instance for storing the processed data.
2.  **Embedding**: Using a sentence-transformer model to create vector embeddings for the `text` field of each JSON object.
3.  **Ingestion**: Writing a script to load the flattened, enriched, and embedded data into the vector database.
4.  **RAG Pipeline Development**: Building the core RAG application using a framework like LangChain to orchestrate retrieval, context assembly, and generation with an LLM.
