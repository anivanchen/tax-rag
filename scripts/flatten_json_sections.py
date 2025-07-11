import json
import datetime

def flatten_section_completely(section, base_metadata):
    """
    Flattens an entire section (including all subsections) into a single document.
    """
    original_id = section['id']
    version_date = base_metadata['version_date']
    legislation_type = base_metadata['legislation_type']
    
    # Build the complete text content by concatenating section text and all subsection text
    text_parts = []
    
    # Add the main section text if it exists
    section_text = section.get('text', '').strip()
    if section_text:
        text_parts.append(section_text)
    
    # Recursively collect all subsection text
    def collect_subsection_text(node, level=1):
        """Recursively collect text from all subsections"""
        for subsection in node.get('subsections', []):
            subsection_text = subsection.get('text', '').strip()
            if subsection_text:
                # Add some formatting to distinguish subsection levels
                indent = "  " * level
                subsection_code = subsection.get('code', subsection.get('id', ''))
                formatted_text = f"{indent}{subsection_code} {subsection_text}"
                text_parts.append(formatted_text)
            
            # Recursively process nested subsections
            collect_subsection_text(subsection, level + 1)
    
    collect_subsection_text(section)
    
    # Join all text parts
    complete_text = "\n\n".join(text_parts)
    
    # Build breadcrumb for the section
    title_name = base_metadata['title']
    chapter_number = base_metadata['chapter_number']
    chapter_title = base_metadata['chapter_title']
    section_name = base_metadata['section_name']
    
    breadcrumb = f"{title_name} > Chapter {chapter_number}: {chapter_title} > {section_name}"
    
    metadata = base_metadata.copy()
    metadata['original_id'] = original_id
    metadata['full_citation'] = f"{legislation_type} § {original_id}"
    metadata['breadcrumb'] = breadcrumb
    metadata['chunk_size'] = len(complete_text)
    metadata['keywords'] = []
    metadata['summary'] = ""
    metadata['status'] = "Active"
    metadata['supersedes_uid'] = ""
    metadata['source_legislation_uid'] = ""
    
    # Count subsections for additional metadata
    def count_subsections(node):
        """Count total number of subsections recursively"""
        count = len(node.get('subsections', []))
        for subsection in node.get('subsections', []):
            count += count_subsections(subsection)
        return count
    
    metadata['total_subsections'] = count_subsections(section)
    metadata['has_subsections'] = len(section.get('subsections', [])) > 0
    
    # Hyphenate legislation_type for the UID
    legislation_type_hyphenated = legislation_type.replace(' ', '-')
    
    doc = {
        'uid': f"{legislation_type_hyphenated}_{original_id}_{version_date}",
        'text': complete_text,
        'metadata': metadata
    }
    
    return doc

def flatten_json_by_sections(input_filename, output_filename, version_date):
    """
    Reads a hierarchical JSON file and flattens it by complete sections 
    (one document per section, including all subsections).
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

            for section in chapter.get('sections', []):
                # Skip if section is empty or has no ID
                if not section or 'id' not in section:
                    continue

                # Base metadata for the section
                base_metadata = {
                    'title': title_name,
                    'chapter_number': chapter_number,
                    'chapter_title': chapter_title,
                    'section_number': section.get('section_number', ''),
                    'section_name': section.get('section_name', ''),
                    'version_date': version_date,
                    'legislation_type': 'NYC Admin Code'
                }
                
                # Flatten the entire section into a single document
                doc = flatten_section_completely(section, base_metadata)
                
                # Only add the document if it has text content
                if doc['text'].strip():
                    flat_documents.append(doc)

    # Write the flattened data to the output file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(flat_documents, f, indent=4)

    return len(flat_documents)

if __name__ == "__main__":
    # Get the current date for versioning
    today = datetime.date.today()
    version_date = today.strftime('%Y-%m-%d')

    # Define input and output filenames
    input_filename = '../data/nyc_tax_code.json'
    output_filename = f'../data/nyc_tax_code_sections_flat_{version_date.replace('-', '')}.json'

    document_count = flatten_json_by_sections(input_filename, output_filename, version_date)
    print(f"Section-level flattening complete. Created {document_count} documents.")
    print(f"The data has been saved to {output_filename}")
