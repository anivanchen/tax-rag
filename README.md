# NYC Administrative Code Parser

This project contains a Python script to parse the New York City Administrative Code from an HTML file (`nyc-admin-code.html`) and convert it into a structured JSON format (`nyc_tax_code.json`).

## Setup

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

## Usage

To parse the HTML file and generate the JSON output, run the script from the root directory:

```bash
python3 parse_code.py
```

The script will create a `nyc_tax_code.json` file containing the parsed data.

## How the Parser Works

The core of this project is the `parse_code.py` script, which uses the `BeautifulSoup` library to interpret the HTML structure of the administrative code.

### Overall Structure

The script performs the following steps:
1.  Reads the `nyc-admin-code.html` file.
2.  Uses `BeautifulSoup` to parse the HTML.
3.  Identifies all major structural `<div>` elements based on their CSS classes (`Title`, `Chapter`, `Section`, `Normal-Level`).
4.  Iterates through these elements to build a hierarchical Python dictionary.
5.  Dumps this dictionary into a JSON file.

### In-Depth Parsing Logic

The most complex part of the script is handling the hierarchical nesting of sections and subsections. The script maintains a state and intelligently determines the relationship between different pieces of text based on their HTML structure and indentation.

1.  **Identifying Structural Elements**: The script begins by finding all `<div>` tags with the classes `Title`, `Chapter`, `Section`, and `Normal-Level`. These classes reliably mark the different parts of the legal code.

2.  **Top-Level Parsing**:
    *   When a `div` with class `Title` is encountered, a new title object is created.
    *   When a `div` with class `Chapter` is found, it's added to the current title.
    *   When a `div` with class `Section` is found, it's added to the current chapter. At this point, a crucial list called `subsection_tracker` is initialized.

3.  **Hierarchical Subsection Parsing (`Normal-Level` divs)**:
    The `subsection_tracker` is the key to managing the nested structure. It acts as a stack, keeping track of the current path in the hierarchy. Each item in the tracker is a dictionary containing the indentation level and the subsection object itself.

    For each `Normal-Level` div, the script does the following:
    *   **Measures Indentation**: It calculates the indentation of the text by counting the number of non-breaking space characters (`&nbsp;` or `\xa0`) at the beginning of the line. This indentation is a reliable indicator of the subsection's depth.
    *   **Identifies Subsections**: It uses a regular expression (`re.match`) to check if the line starts with a subsection marker (e.g., `(a)`, `1.`, `(i)`).
    *   **Places Subsections in the Hierarchy**:
        *   If the text is a subsection, the script uses the `subsection_tracker` to find its correct parent. It does this by comparing the current line's indentation with the indentation of the last item in the tracker.
        *   The `while` loop pops items off the `subsection_tracker` stack until it finds an item with a smaller indentation level. This item is the parent of the current subsection.
        *   If the tracker becomes empty, it means the new subsection is a direct child of the main section.
        *   Otherwise, it's appended to the `subsections` list of its parent.
        *   Finally, the new subsection is pushed onto the `subsection_tracker` stack, becoming the new potential parent for any subsequent, deeper subsections.
    *   **Handles Content Text**: If a line is not a subsection marker, its text content is appended to the `text` field of the most recent subsection (the last item in the `subsection_tracker`). If there are no active subsections, the text is appended to the main section's text.
