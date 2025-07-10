# JSON Flattening Script (`flatten_json.py`)

This document provides an overview of the `scripts/flatten_json.py` script, which is designed to transform the hierarchical JSON data from `data/nyc_tax_code.json` into a flat structure suitable for ingestion into a vector database for a Retrieval-Augmented Generation (RAG) system.

## Purpose

The primary goal of this script is to convert a deeply nested JSON file, representing the structure of the NYC Administrative Code, into a simple list of JSON objects. Each object, or "document," represents a single, discrete section or subsection of the code, making it ideal for semantic search and retrieval.

## Usage

The script is intended to be run from the `scripts` directory after `parse_code.py` has generated the `data/nyc_tax_code.json` file.

```bash
python3 flatten_json.py
```

This will produce a new, versioned file named `nyc_tax_code_flat_YYYYMMDD.json` in the `data` directory.

## How It Works

The script reads the `data/nyc_tax_code.json` file and traverses its structure to create a flattened list of documents.

### 1. Main Function (`flatten_json_granular`)

-   **Loads Data**: The script starts by loading the source JSON file.
-   **Iterates through Hierarchy**: It iterates through the top-level `titles`, then `chapters`, and finally `sections`.
-   **Creates Base Metadata**: For each section, it creates a `base_metadata` dictionary containing information that is common to the section and all of its children (subsections). This includes title, chapter details, and section details.
-   **Initiates Recursion**: It then calls the `flatten_recursively` function to process the section and all of its nested subsections.

### 2. Recursive Flattening (`flatten_recursively`)

This function is the core of the flattening logic. It takes a "node" (which can be a section or a subsection) and recursively processes it and its children.

-   **Creates a Document**: For each node, it creates a distinct JSON object.
-   **Builds Metadata**: It populates the `metadata` for the document, including:
    -   A `breadcrumb` trail to show its position in the hierarchy (e.g., "Title > Chapter > Section > Subsection").
    -   A unique `uid` for the document.
    -   A `full_citation`.
    -   Placeholders for future enrichment (`keywords`, `summary`).
    -   Versioning fields (`status`, `supersedes_uid`, `source_legislation_uid`).
-   **Recurses**: It then calls itself for each of the node's `subsections`, passing along the `base_metadata` and the updated `breadcrumb`.

## Output Data Structure

The output is a single JSON array where each object has the following structure:

```json
{
    "uid": "string",
    "text": "string",
    "metadata": {
        "title": "string",
        "chapter_number": "string",
        "chapter_title": "string",
        "section_number": "string",
        "section_name": "string",
        "version_date": "YYYY-MM-DD",
        "legislation_type": "string",
        "original_id": "string",
        "full_citation": "string",
        "breadcrumb": "string",
        "chunk_size": "integer",
        "keywords": [],
        "summary": "string",
        "status": "string",
        "supersedes_uid": "string",
        "source_legislation_uid": "string"
    }
}
```

### Key Fields Explained

-   **`uid`**: A unique identifier for the document, constructed from the legislation type, the original ID, and the version date.
-   **`text`**: The actual text content of the section or subsection.
-   **`metadata`**: A collection of all other relevant information.
    -   **`original_id`**: The ID from the source document (e.g., "11-128.b").
    -   **`full_citation`**: A legal-style citation (e.g., "NYC Admin Code § 11-128.b").
    -   **`breadcrumb`**: The full hierarchical path to the document.
    -   **`chunk_size`**: The character length of the `text` field.
    -   **`status`**: The current status of the document.
        - **Active**: Currently in-force version.
        - **Superseded**: Older version replaced with new one.
        - **Repealed**: Completely removed version.
        - **Future_Effective**: Amended or created but will only be effective in the future.
        - **Draft**: Pre-enactment stage.
    -   **`supersedes_uid`**: The `uid` of the document that this version replaces.
    -   **`source_legislation_uid`**: The `uid` of the amendment or law that created this version.
