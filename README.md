# NYC Tax Code RAG Project

This project provides a comprehensive toolkit for parsing, processing, and searching the New York City Administrative Code for Taxation and Finance (Title 11). It implements a full Retrieval-Augmented Generation (RAG) pipeline, from initial data parsing to vectorized search, and includes tools for analyzing different data chunking strategies.

## Key Features

- **HTML to JSON Parsing**: Converts the complex, nested HTML structure of the tax code into a clean, hierarchical JSON format.
- **Dual Flattening Approaches**: Implements two distinct methods for preparing data for a vector database:
    1.  **Granular (Recursive)**: Each section and subsection is treated as an individual document.
    2.  **Section-Level**: Each top-level section is a single document, with all its subsections concatenated.
- **Vectorized Database Ingestion**: Ingests the flattened documents into a [ChromaDB](https://www.trychroma.com/) vector store.
- **Semantic Search**: Provides scripts to perform semantic searches on both the granular and section-level collections.
- **Performance Analysis**: Includes a sophisticated script to compare the performance, speed, and search quality of the two flattening approaches across various query types.

## Project Structure

```
nyc-tax/
├── data/
│   ├── nyc-tax-code.html         # Raw HTML source
│   ├── nyc_tax_code.json         # Parsed, structured JSON
│   ├── nyc_tax_code_flat_*.json  # Granular flattened data
│   ├── nyc_tax_code_sections_flat_*.json # Section-level flattened data
│   └── chroma_db/                # ChromaDB vector store
├── docs/
│   └── *.md                      # Project documentation and plans
├── env/
│   └── ...                       # Python virtual environment
├── scripts/
│   ├── parse_code.py             # Parses HTML to structured JSON
│   ├── flatten_json.py           # Flattens JSON recursively (granular)
│   ├── flatten_json_sections.py  # Flattens JSON by section
│   ├── ingest_data.py            # Ingests granular data into ChromaDB
│   ├── ingest_data_sections.py   # Ingests section-level data into ChromaDB
│   ├── search_data.py            # Searches the granular collection
│   ├── search_data_sections.py   # Searches the section-level collection
│   └── performance_analysis.py   # Compares performance of both approaches
└── README.md
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd nyc-tax
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Workflow and Usage

Follow these steps to set up the database and run searches. The scripts should be run from within the `scripts/` directory.

```bash
cd scripts/
```

### Step 1: Parse the Raw HTML

First, parse the source HTML file (`data/nyc-tax-code.html`) into a structured JSON file.

```bash
python parse_code.py
```
- **Input**: `data/nyc-tax-code.html`
- **Output**: `data/nyc_tax_code.json`

### Step 2: Flatten the JSON Data

Next, create the flattened document files for ingestion. You can generate one or both versions.

**Option A: Granular (Recursive) Flattening**
```bash
python flatten_json.py
```
- **Input**: `data/nyc_tax_code.json`
- **Output**: `data/nyc_tax_code_flat_YYYYMMDD.json`

**Option B: Section-Level Flattening**
```bash
python flatten_json_sections.py
```
- **Input**: `data/nyc_tax_code.json`
- **Output**: `data/nyc_tax_code_sections_flat_YYYYMMDD.json`

### Step 3: Ingest Data into ChromaDB

Ingest the flattened files into their respective ChromaDB collections.

**Option A: Ingest Granular Data**
```bash
python ingest_data.py
```
- **Collection Name**: `nyc_tax_code`
- **Documents**: ~8,000

**Option B: Ingest Section-Level Data**
```bash
python ingest_data_sections.py
```
- **Collection Name**: `nyc_tax_code_sections`
- **Documents**: ~800

### Step 4: Search the Database

Query the collections using the search scripts.

**Option A: Search Granular Collection**
```bash
python search_data.py "your search query here"
```

**Option B: Search Section-Level Collection**
```bash
python search_data_sections.py "your search query here"
```
You can also specify the number of results to return with the `-n` flag:
```bash
python search_data.py "real estate transfer tax" -n 10
```

### Step 5: Manual Search and Evaluation

With the data ingested, you can now manually test and evaluate the search quality of each approach. This is crucial for understanding the trade-offs between semantic relevance and chunking strategy.

**Search Granular Collection:**
```bash
python search_data.py "your search query"
```

**Search Section-Level Collection:**
```bash
python search_data_sections.py "your search query"
```

Focus on how the results differ for various types of queries (broad, specific, technical) to determine which chunking strategy best suits your needs.

## Future Directions and Roadmap

This project is an ongoing effort to build a robust and intelligent RAG system for legal documents. The current foundation enables several exciting future developments:

### 1. Advanced Chunking and Enrichment
- **Explore New Chunking Techniques**: Move beyond granular and section-level strategies to explore more advanced methods like semantic chunking or proposition-based chunking.
- **AI-Generated Keywords**: Implement a lightweight AI/summarization model to automatically generate relevant keywords for each data entry, enhancing metadata and filterability.
- **Metadata Refinement**: Re-evaluate the metadata structure, potentially removing the summary section in favor of more dynamic, AI-generated fields.

### 2. Expanding the Knowledge Base
- **Incorporate NYS Tax Code**: Expand the data sources to include New York State tax law, creating a more comprehensive legal database.
- **Dynamic Legislative Updates**: Develop a robust system for managing the lifecycle of legal documents:
    - **Add**: Seamlessly integrate new legislation.
    - **Deprecate**: Mark outdated laws as no longer in effect while retaining them for historical context.
    - **Delete**: Remove irrelevant or superseded entries.
- **Automated Re-ingestion**: Create a process to periodically re-ingest the entire tax code to ensure the database remains current and fresh.

### 3. Building a Full RAG Pipeline
- **Embedding Model Evaluation**: Benchmark and evaluate different text embedding models to find the optimal balance of performance, cost, and semantic understanding.
- **Intelligent Query Parsing**: Develop a component that can parse natural language user questions into structured search queries, complete with metadata filters, to improve search accuracy.
- **End-to-End Implementation**: Build out the complete RAG pipeline, connecting the user interface, query parser, retriever (ChromaDB), and a language model for generating answers.
