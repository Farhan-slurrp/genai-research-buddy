from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer

def scrape_webpage(url: str) -> str:
  loader = AsyncHtmlLoader([url])
  docs = loader.load()
  html2text = Html2TextTransformer()
  docs_transformed = html2text.transform_documents(docs)
  return docs_transformed

tool_scrape_webpage = {
  'type':'function', 
  'function':{
    'name': 'scrape_webpage',
    'description': 'Scrapes the content of a given webpage URL',
    'parameters': {
            'type': 'object',
            'properties': {
                'url': {
                    'type': 'string',
                    'description': 'The URL of the web page to scrape.',
                },
            },
            'required': ['url'],
        },
    }
}