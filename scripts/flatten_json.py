import json
import datetime

def flatten_recursively(node, documents, base_metadata, breadcrumb=""):
    """
    Recursively traverses nodes, creating a flat document for each node.
    """
    # Create a document for the current node
    original_id = node['id']
    version_date = base_metadata['version_date']
    legislation_type = base_metadata['legislation_type']
    
    # Build breadcrumb
    node_identifier = node.get('code', '').strip() or node.get('id')
    new_breadcrumb = f"{breadcrumb} > {node_identifier}" if breadcrumb else base_metadata.get('section_name', '')

    metadata = base_metadata.copy()
    metadata['original_id'] = original_id
    metadata['full_citation'] = f"{legislation_type} § {original_id}"
    metadata['breadcrumb'] = new_breadcrumb

    # Hyphenate legislation_type for the UID
    legislation_type_hyphenated = legislation_type.replace(' ', '-')

    text_content = node.get('text', '').strip()

    metadata['chunk_size'] = len(text_content)
    metadata['keywords'] = []
    metadata['summary'] = ""
    metadata['status'] = "Active"
    metadata['supersedes_uid'] = ""
    metadata['source_legislation_uid'] = ""

    doc = {
        'uid': f"{legislation_type_hyphenated}_{original_id}_{version_date}",
        'text': text_content,
        'metadata': metadata
    }
    
    # Only add the document if it has text content
    if doc['text']:
        documents.append(doc)

    # Recursively process subsections
    for sub in node.get('subsections', []):
        # For subsections, the base_metadata is the same
        flatten_recursively(sub, documents, base_metadata, breadcrumb=new_breadcrumb)

def flatten_json_granular(input_filename, output_filename, version_date):
    """
    Reads a hierarchical JSON file, flattens it into granular documents, 
    and writes the result to a new file.
    """
    with open(input_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    flat_documents = []

    # Iterate through the hierarchical structure
    for title in data.get('titles', []):
        title_name = title.get("title_name", "")
        for chapter in title.get('chapters', []):
            chapter_name_full = chapter.get("chapter_name", "")
            chapter_number = ''
            chapter_title = chapter_name_full
            if ': ' in chapter_name_full:
                try:
                    chapter_number_str, chapter_title_str = chapter_name_full.split(': ', 1)
                    if 'Chapter' in chapter_number_str:
                        chapter_number = chapter_number_str.replace('Chapter', '').strip()
                        chapter_title = chapter_title_str.strip()
                except ValueError:
                    # Handle cases where split doesn't work as expected
                    pass
            
            initial_breadcrumb = f"{title_name} > Chapter {chapter_number}: {chapter_title}"

            for section in chapter.get('sections', []):
                # Skip if section is empty
                if not section or 'id' not in section:
                    continue

                # Base metadata for the section and all its subsections
                base_metadata = {
                    'title': title_name,
                    'chapter_number': chapter_number,
                    'chapter_title': chapter_title,
                    'section_number': section.get('section_number', ''),
                    'section_name': section.get('section_name', ''),
                    'version_date': version_date,
                    'legislation_type': 'NYC Admin Code'
                }
                
                # Process the section and its subsections
                flatten_recursively(section, flat_documents, base_metadata, breadcrumb=initial_breadcrumb)

    # Write the flattened data to the output file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(flat_documents, f, indent=4)

if __name__ == "__main__":

    # Get the current date for versioning
    today = datetime.date.today()
    version_date = today.strftime('%Y-%m-%d')

    # Define input and output filenames
    input_filename = '../data/nyc_tax_code.json'
    output_filename = f'../data/nyc_tax_code_flat_{version_date.replace('-', '')}.json'

    flatten_json_granular(input_filename, output_filename, version_date)
    print(f"Flattening complete. The data has been saved to {output_filename}")
