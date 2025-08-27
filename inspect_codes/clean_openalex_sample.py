import csv
import json
import os

INPUT_CSV = 'data/openalex_sample.csv'
OUTPUT_DIR = 'data/cleaned_papers'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def reconstruct_abstract(abstract_dict):
    # abstract_dict: {word: [indexes]}
    if not abstract_dict:
        return ''
    # Find max index
    all_idx = []
    for idxs in abstract_dict.values():
        all_idx.extend(idxs)

    max_index = max(all_idx)
    # print(max_index)
    # exit(1)
    abstract_words = [''] * (max_index + 1)
    for word, idxs in abstract_dict.items():
        for idx in idxs:
            abstract_words[idx] = word
    return ' '.join(abstract_words)

def parse_authors(authors_str):
    # Expecting a stringified list of dicts
    try:
        authors = json.loads(authors_str.replace("'", '"'))
        result = []
        # print(authors)
        for author in authors:
            # print(author)
            # author_info = author.get('author')
            # print(author_info)
            # print(author)
            # exit(1)
            name = author['raw_author_name']
            # print(name)
            affiliation = author['affiliations'][0]['raw_affiliation_string'] # for now, only first affiliation is used
            # print(affiliation)
            # affiliation = author.get('affiliation', '') or author.get('institute', '')
            result.append({'name': name, 'affiliation': affiliation})
        return result
    except Exception:
        return []

def main():
    with open(INPUT_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            # print(row)
            paper = {}
            paper['title'] = row.get('title', '')
            # print(paper)
            # exit(1)
            paper['authors'] = parse_authors(row.get('authorships', ''))
            # print(paper['authors'])
            # exit(1)
            paper['publication_date'] = row.get('publication_date', '')
            # print(row)
            # print(paper['publication_date'])
            # exit(1)
            # Parse abstract
            abstract_str = row.get('abstract_inverted_index', '{}')
            try:
                abstract_dict = json.loads(abstract_str.replace("'", '"'))
            except Exception:
                abstract_dict = {}
            # print(abstract_dict)
            # exit(1)
            paper['abstract'] = reconstruct_abstract(abstract_dict)
            # print(paper['abstract'])
            # Save to JSON
            out_path = os.path.join(OUTPUT_DIR, f'paper_{i+1}.json')
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(paper, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
