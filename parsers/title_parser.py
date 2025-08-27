"""
Parser for OpenAlex title information.
"""


def parse_title(display_name):
    """
    Parse title from OpenAlex display_name field.
    
    Args:
        display_name: String containing the paper title
        
    Returns:
        String containing the cleaned title
    """
    if not display_name:
        return ''
    
    return display_name.strip()
