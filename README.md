# OpenAlex Paper Processor

A modular system for processing OpenAlex JSONL files into structured JSON format using customizable parsers.

## Features

- **Modular Parser Architecture**: Individual parsers for different data fields
- **Customizable Field Selection**: Choose which fields to extract and how to process them
- **Single JSON Output**: All papers saved in one JSON file (no intermediate files)
- **Error Handling**: Robust error handling with warnings for problematic records
- **Extensible**: Easy to add new parsers for additional fields

## Directory Structure

```
LLM-Paper-reviewer/
├── openalex_processor.py          # Main processing function
├── example_usage.py               # Usage examples
├── parsers/                       # Parser modules
│   ├── __init__.py               # Package initialization
│   ├── authors_parser.py         # Author information parser
│   ├── abstract_parser.py        # Abstract reconstruction parser
│   ├── date_parser.py            # Publication date parser
│   └── title_parser.py           # Title parser
└── data/
    ├── raw_openalex.jsonl        # Input JSONL file
    └── processed_papers.json     # Output JSON file
```

## Basic Usage

```python
from openalex_processor import process_openalex_papers, create_default_field_parsers

# Use default parsers for common fields
field_parsers = create_default_field_parsers()

process_openalex_papers(
    'data/raw_openalex.jsonl',
    'data/processed_papers.json',
    field_parsers
)
```

## Custom Parser Configuration

```python
from parsers.authors_parser import parse_authors
from parsers.abstract_parser import parse_abstract
from parsers.date_parser import parse_publication_date
from parsers.title_parser import parse_title

# Define custom field parsers
custom_field_parsers = {
    'title': lambda record: parse_title(record.get('display_name', '')),
    'authors': lambda record: parse_authors(record.get('authorships', [])),
    'abstract': lambda record: parse_abstract(record.get('abstract_inverted_index', {})),
    'publication_date': lambda record: parse_publication_date(record.get('publication_date', '')),
    'year': lambda record: record.get('publication_date', '')[:4],  # Extract year only
}

process_openalex_papers(
    'data/raw_openalex.jsonl',
    'data/custom_processed_papers.json',
    custom_field_parsers
)
```

## Available Parsers

### `parse_authors(authorships_data)`
Extracts author information from OpenAlex authorships field.

**Input**: List of authorship dictionaries
**Output**: List of author dictionaries with 'name' and 'affiliation' fields

### `parse_abstract(abstract_inverted_index)`
Reconstructs readable abstract from OpenAlex inverted index format.

**Input**: Dictionary with words as keys and position lists as values
**Output**: String containing the reconstructed abstract

### `parse_publication_date(publication_date)`
Formats publication date consistently.

**Input**: String in 'YYYY-MM-DD' format
**Output**: Formatted date string

### `parse_title(display_name)`
Extracts and cleans paper title.

**Input**: String containing the paper title
**Output**: Cleaned title string

## Creating Custom Parsers

To create a new parser, follow this pattern:

```python
# parsers/my_custom_parser.py
def parse_my_field(field_data):
    """
    Parse custom field from OpenAlex data.
    
    Args:
        field_data: Raw field data from OpenAlex record
        
    Returns:
        Processed field data
    """
    if not field_data:
        return None
    
    # Your processing logic here
    processed_data = process_field_data(field_data)
    
    return processed_data
```

Then use it in your field parsers dictionary:

```python
from parsers.my_custom_parser import parse_my_field

field_parsers = {
    'my_field': lambda record: parse_my_field(record.get('field_name', '')),
    # ... other parsers
}
```

## Error Handling

The processor includes robust error handling:
- Warnings for records that can't be parsed
- Graceful degradation for individual field parsing errors
- Continuation of processing even when some records fail

## Running Examples

```bash
python3 example_usage.py
```

This will create several example output files demonstrating different parser configurations:
- `basic_processed_papers.json` - Default parsers
- `custom_processed_papers.json` - Custom parser example
- `minimal_processed_papers.json` - Minimal fields only
- `extended_processed_papers.json` - Extended fields with additional data

## Function Signature

```python
def process_openalex_papers(input_jsonl_path, output_json_path, field_parsers):
    """
    Process OpenAlex papers from JSONL format to structured JSON.
    
    Args:
        input_jsonl_path (str): Path to the input OpenAlex JSONL file
        output_json_path (str): Path to save the output JSON file
        field_parsers (dict): Dictionary mapping output field names to parser functions
                             Format: {'output_field_name': parser_function}
    """
```

## Migration from Old System

The new system replaces the three separate scripts (`inspect_openalex_output.py`, `export_openalex_sample.py`, `clean_openalex_sample.py`) with a single, more flexible solution that:

1. Processes directly from JSONL to JSON (no intermediate CSV)
2. Uses modular parsers for better maintainability
3. Allows custom field selection and processing
4. Handles errors more gracefully
5. Provides a consistent API for future extensions
