"""
Parser for OpenAlex publication date information.
"""
from datetime import datetime


def parse_publication_date(publication_date):
    """
    Parse publication date from OpenAlex format.
    
    Args:
        publication_date: String in format 'YYYY-MM-DD' or other format
        
    Returns:
        String containing the formatted publication date
    """
    if not publication_date:
        return ''
    
    try:
        # Try to parse and reformat the date to ensure consistency
        parsed_date = datetime.strptime(publication_date, "%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%d")
    except Exception:
        # If parsing fails, return the original string
        return publication_date
