"""
Example usage of the OpenAlex processor with custom parsers.

This script demonstrates how to use the modular OpenAlex processor
with different parser configurations.
"""
from openalex_processor import process_openalex_papers, create_default_field_parsers
from parsers.authors_parser import parse_authors
from parsers.abstract_parser import parse_abstract
from parsers.date_parser import parse_publication_date
from parsers.title_parser import parse_title


def example_basic_usage():
    """Example 1: Basic usage with default parsers."""
    print("=== Example 1: Basic usage with default parsers ===")
    
    # Use default field parsers
    field_parsers = create_default_field_parsers()
    
    process_openalex_papers(
        'data/raw_openalex.jsonl',
        'data/basic_processed_papers.json',
        field_parsers
    )


def example_custom_parsers():
    """Example 2: Custom parser configuration."""
    print("\n=== Example 2: Custom parser configuration ===")
    
    # Custom parser that only extracts title and first author
    def parse_first_author_only(authorships_data):
        """Extract only the first author."""
        authors = parse_authors(authorships_data)
        return authors[0] if authors else None
    
    # Custom parser for short abstract (first 100 characters)
    def parse_short_abstract(abstract_inverted_index):
        """Extract short version of abstract."""
        full_abstract = parse_abstract(abstract_inverted_index)
        return full_abstract[:100] + "..." if len(full_abstract) > 100 else full_abstract
    
    custom_field_parsers = {
        'title': lambda record: parse_title(record.get('display_name', '')),
        'first_author': lambda record: parse_first_author_only(record.get('authorships', [])),
        'short_abstract': lambda record: parse_short_abstract(record.get('abstract_inverted_index', {})),
        'year': lambda record: parse_publication_date(record.get('publication_date', ''))[:4] if record.get('publication_date') else '',
    }
    
    process_openalex_papers(
        'data/raw_openalex.jsonl',
        'data/custom_processed_papers.json',
        custom_field_parsers
    )


def example_minimal_parsers():
    """Example 3: Minimal parser configuration (title only)."""
    print("\n=== Example 3: Minimal parser configuration ===")
    
    minimal_field_parsers = {
        'title': lambda record: parse_title(record.get('display_name', '')),
    }
    
    process_openalex_papers(
        'data/raw_openalex.jsonl',
        'data/minimal_processed_papers.json',
        minimal_field_parsers
    )


def example_extended_parsers():
    """Example 4: Extended parser configuration with additional fields."""
    print("\n=== Example 4: Extended parser configuration ===")
    
    # Parser for related works
    def parse_related_works(related_works_data):
        """Parse related works URLs."""
        if not related_works_data:
            return []
        return related_works_data[:5]  # Limit to first 5 related works
    
    # Parser for author count
    def parse_author_count(authorships_data):
        """Count number of authors."""
        return len(authorships_data) if authorships_data else 0
    
    extended_field_parsers = {
        'title': lambda record: parse_title(record.get('display_name', '')),
        'authors': lambda record: parse_authors(record.get('authorships', [])),
        'abstract': lambda record: parse_abstract(record.get('abstract_inverted_index', {})),
        'publication_date': lambda record: parse_publication_date(record.get('publication_date', '')),
        'author_count': lambda record: parse_author_count(record.get('authorships', [])),
        'related_works': lambda record: parse_related_works(record.get('related_works', [])),
        'openalex_id': lambda record: record.get('id', ''),
    }
    
    process_openalex_papers(
        'data/raw_openalex.jsonl',
        'data/extended_processed_papers.json',
        extended_field_parsers
    )


if __name__ == '__main__':
    # Run all examples
    example_basic_usage()
    example_custom_parsers()
    example_minimal_parsers()
    example_extended_parsers()
    
    print("\n=== All examples completed! ===")
    print("Check the following output files:")
    print("- data/basic_processed_papers.json")
    print("- data/custom_processed_papers.json")
    print("- data/minimal_processed_papers.json")
    print("- data/extended_processed_papers.json")
