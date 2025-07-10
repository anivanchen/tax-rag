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
            current_title = {
                "title_name": tag.get_text(strip=True),
                "chapters": []
            }
            parsed_data["titles"].append(current_title)
            current_chapter = None
            current_section = None
        
        elif 'Chapter' in tag.get('class', []):
            if current_title is None:
                # Handle case where a chapter appears before a title
                current_title = { "title_name": "Unknown Title", "chapters": [] }
                parsed_data["titles"].append(current_title)

            current_chapter = {
                "chapter_name": tag.get_text(strip=True),
                "sections": []
            }
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

            current_section = {
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
                    
                    new_subsection = {
                        "code": code,
                        "text": sub_text,
                        "subsections": []
                    }

                    while subsection_tracker and indentation <= subsection_tracker[-1]['indentation']:
                        subsection_tracker.pop()
                    
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
    parsed_structure = parse_nyc_admin_code_html('nyc-tax-code.html')
    with open('nyc_tax_code.json', 'w') as f:
        json.dump(parsed_structure, f, indent=4)
    print("Parsing complete. The structured data has been saved to nyc_tax_code.json")
