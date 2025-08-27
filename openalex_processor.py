"""
General OpenAlex paper processor.

This module provides a general function to process OpenAlex JSONL files
and convert them to structured JSON format using modular parsers.
"""
import json
import orjson
from pathlib import Path


def process_openalex_papers(input_jsonl_path, output_json_path, field_parsers):
    """
    Process OpenAlex papers from JSONL format to structured JSON.
    
    Args:
        input_jsonl_path (str): Path to the input OpenAlex JSONL file
        output_json_path (str): Path to save the output JSON file
        field_parsers (dict): Dictionary mapping output field names to parser functions
                             Format: {'output_field_name': parser_function}
                             
    Example:
        from parsers.authors_parser import parse_authors
        from parsers.abstract_parser import parse_abstract
        from parsers.date_parser import parse_publication_date
        from parsers.title_parser import parse_title
        
        field_parsers = {
            'title': lambda record: parse_title(record.get('display_name', '')),
            'authors': lambda record: parse_authors(record.get('authorships', [])),
            'abstract': lambda record: parse_abstract(record.get('abstract_inverted_index', {})),
            'publication_date': lambda record: parse_publication_date(record.get('publication_date', ''))
        }
        
        process_openalex_papers('data/raw_openalex.jsonl', 'data/processed_papers.json', field_parsers)
    """
    input_path = Path(input_jsonl_path)
    output_path = Path(output_json_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    papers = []
    
    try:
        with open(input_path, 'rb') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    # Parse JSON record
                    record = orjson.loads(line)
                    
                    # Process record using provided parsers
                    paper = {}
                    for output_field, parser_func in field_parsers.items():
                        try:
                            paper[output_field] = parser_func(record)
                        except Exception as e:
                            print(f"Warning: Error parsing field '{output_field}' for record {line_num}: {e}")
                            paper[output_field] = None
                    
                    papers.append(paper)
                    
                except Exception as e:
                    print(f"Warning: Error processing record {line_num}: {e}")
                    continue
        
        # Save all papers to single JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully processed {len(papers)} papers from {input_path} to {output_path}")
        
    except FileNotFoundError:
        print(f"Error: Input file {input_path} not found")
        raise
    except Exception as e:
        print(f"Error processing file: {e}")
        raise


def create_default_field_parsers():
    """
    Create a default set of field parsers for common OpenAlex fields.
    
    Returns:
        dict: Default field parsers dictionary
    """
    from parsers.authors_parser import parse_authors
    from parsers.abstract_parser import parse_abstract
    from parsers.date_parser import parse_publication_date
    from parsers.title_parser import parse_title
    
    return {
        'title': lambda record: parse_title(record.get('display_name', '')),
        'authors': lambda record: parse_authors(record.get('authorships', [])),
        'abstract': lambda record: parse_abstract(record.get('abstract_inverted_index', {})),
        'publication_date': lambda record: parse_publication_date(record.get('publication_date', ''))
    }


if __name__ == '__main__':
    # Example usage with default parsers
    field_parsers = create_default_field_parsers()
    
    # Process the existing OpenAlex file
    process_openalex_papers(
        'data/raw_openalex.jsonl',
        'data/processed_papers.json',
        field_parsers
    )
