"""
Parser for OpenAlex author information.
"""
import json


def parse_authors(authorships_data):
    """
    Parse authorships data from OpenAlex into a structured format.
    
    Args:
        authorships_data: List of authorship dictionaries from OpenAlex
        
    Returns:
        List of author dictionaries with name and affiliation
    """
    if not authorships_data:
        return []
    
    result = []
    try:
        for author in authorships_data:
            name = author.get('raw_author_name', '')
            # Get first affiliation if available
            affiliation = ''
            affiliations = author.get('affiliations', [])
            if affiliations and len(affiliations) > 0:
                affiliation = affiliations[0].get('raw_affiliation_string', '')
            
            result.append({
                'name': name,
                'affiliation': affiliation
            })
        return result
    except Exception as e:
        print(f"Warning: Error parsing authors: {e}")
        return []
