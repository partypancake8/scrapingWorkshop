# pip install firecrawl-py

import json
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-d2612b97887e49fe9b9464a597b99ee6")


response = firecrawl.crawl('https://swyr.com',
    limit=10,
    scrape_options={
        'formats': [
            'markdown',
            { 'type': 'json', 'schema': { 'type': 'object', 'properties': { 'title': { 'type': 'string' } } } }
        ],
        'proxy': 'auto',
        'maxAge': 600000,
        'onlyMainContent': True
    }
)

# The crawl response contains a 'data' attribute with the list of documents
docs = response.data if hasattr(response, 'data') else []

print(f"Number of pages crawled: {len(docs)}")

# Export each crawled page to a separate JSON file
for i, doc in enumerate(docs):
    filename = f"exported_page_{i+1}.json"
    
    # Create a dictionary with all the document data
    page_data = {
        'url': getattr(doc.metadata, 'source_url', None) if hasattr(doc, 'metadata') else None,
        'title': doc.json.get('title') if hasattr(doc, 'json') and doc.json else None,
        'markdown': doc.markdown if hasattr(doc, 'markdown') else None,
        'json_data': doc.json if hasattr(doc, 'json') else None,
        'metadata': {
            'title': getattr(doc.metadata, 'title', None),
            'description': getattr(doc.metadata, 'description', None),
            'source_url': getattr(doc.metadata, 'source_url', None),
            'status_code': getattr(doc.metadata, 'status_code', None),
        } if hasattr(doc, 'metadata') else None,
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(page_data, f, indent=2, ensure_ascii=False)
    
    print(f"Exported: {filename}")

print(f"\nTotal pages exported: {len(docs)}")