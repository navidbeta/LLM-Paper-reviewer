"""
Parser for OpenAlex abstract information.
"""
import json


def parse_abstract(abstract_inverted_index):
    """
    Parse abstract inverted index from OpenAlex into readable text.
    
    Args:
        abstract_inverted_index: Dictionary with words as keys and position lists as values
        
    Returns:
        String containing the reconstructed abstract
    """
    if not abstract_inverted_index:
        return ''
    
    try:
        # Find max index to determine abstract length
        all_indices = []
        for indices in abstract_inverted_index.values():
            all_indices.extend(indices)
        
        if not all_indices:
            return ''
            
        max_index = max(all_indices)
        
        # Create array to hold words in correct positions
        abstract_words = [''] * (max_index + 1)
        
        # Place words in their correct positions
        for word, indices in abstract_inverted_index.items():
            for idx in indices:
                abstract_words[idx] = word
        
        # Join words into final abstract
        return ' '.join(abstract_words)
    except Exception as e:
        print(f"Warning: Error parsing abstract: {e}")
        return ''
