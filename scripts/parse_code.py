import json
from bs4 import BeautifulSoup
import re

# Parses the NYC admin code from an HTML file
def parse_nyc_admin_code_html(file_path):

    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    
    parsed_data = {
        "titles": []
    }

    current_title = None
    current_chapter = None
    current_section = None

    # Find all relevant tags and process them in order
    all_tags = soup.find_all(['div'], class_=['Title', 'Chapter', 'Section', 'Normal-Level'])

    for tag in all_tags:
        if 'Title' in tag.get('class', []):
            title_text = tag.get_text(strip=True)
            current_title = {
                "title_name": title_text,
                "chapters": []
            }
            title_match = re.search(r'\d+', title_text)
            current_title_id = title_match.group(0) if title_match else 'T'
            parsed_data["titles"].append(current_title)
            current_chapter = None
            current_section = None
        
        elif 'Chapter' in tag.get('class', []):
            if current_title is None:
                # Handle case where a chapter appears before a title
                current_title = { "title_name": "Unknown Title", "chapters": [] }
                current_title_id = 'T'
                parsed_data["titles"].append(current_title)

            chapter_text = tag.get_text(strip=True)
            current_chapter = {
                "chapter_name": chapter_text,
                "sections": []
            }
            chapter_match = re.search(r'\d+', chapter_text)
            current_chapter_id = chapter_match.group(0) if chapter_match else 'C'
            current_title["chapters"].append(current_chapter)
            current_section = None

        elif 'Section' in tag.get('class', []):
            if current_chapter is None:
                # Handle case where a section appears before a chapter
                if current_title is None:
                    current_title = { "title_name": "Unknown Title", "chapters": [] }
                    parsed_data["titles"].append(current_title)
                current_chapter = { "chapter_name": "Unknown Chapter", "sections": [] }
                current_title["chapters"].append(current_chapter)

            section_text = tag.get_text(strip=True)
            match = re.match(r'§\s*([\d\-\.]+)\s*(.*)', section_text)
            if match:
                section_number, section_name = match.groups()
            else:
                section_number, section_name = "Unknown", section_text

            section_id = section_number.strip()
            current_section = {
                "id": section_id,
                "section_number": section_number.strip(),
                "section_name": section_name.strip(),
                "text": "",
                "subsections": []
            }
            current_chapter["sections"].append(current_section)
            subsection_tracker = [] # To track the hierarchy of subsections

        elif 'Normal-Level' in tag.get('class', []):
            if current_section is not None:
                text = tag.get_text()
                
                indentation = 0
                for char in text:
                    if ord(char) == 160: # nbsp
                        indentation += 1
                    else:
                        break
                
                text_stripped = text.strip()

                is_subsection = re.match(r'^(\([a-zA-Z0-9]+\)|[a-zA-Z0-9]+\.)', text_stripped)

                if is_subsection:
                    code = is_subsection.group(1)
                    sub_text = text_stripped[len(code):].strip()
                    
                    while subsection_tracker and indentation <= subsection_tracker[-1]['indentation']:
                        subsection_tracker.pop()

                    # Determine parent ID
                    parent_id = current_section['id']
                    if subsection_tracker:
                        parent_id = subsection_tracker[-1]['subsection']['id']

                    clean_code = re.sub(r'[.()]', '', code)
                    new_subsection = {
                        "id": f"{parent_id}.{clean_code}",
                        "code": code,
                        "text": sub_text,
                        "subsections": []
                    }
                    
                    if not subsection_tracker:
                        current_section["subsections"].append(new_subsection)
                    else:
                        parent_subsection = subsection_tracker[-1]['subsection']
                        parent_subsection["subsections"].append(new_subsection)

                    subsection_tracker.append({'indentation': indentation, 'subsection': new_subsection})
                else:
                    # This text belongs to the last subsection found, or the section itself
                    if subsection_tracker:
                        subsection_tracker[-1]['subsection']['text'] += "\n" + text_stripped
                    else:
                        if current_section["text"]:
                            current_section["text"] += "\n" + text_stripped
                        else:
                            current_section["text"] = text_stripped

    return parsed_data


if __name__ == "__main__":
    input_file = '../data/nyc-tax-code.html'
    output_file = '../data/nyc_tax_code.json'

    parsed_structure = parse_nyc_admin_code_html(input_file)
    with open(output_file, 'w') as f:
        json.dump(parsed_structure, f, indent=4)
    print(f"Parsing complete. The structured data has been saved to {output_file}")
