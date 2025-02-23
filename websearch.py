from langchain_community.tools import DuckDuckGoSearchResults

def search_web(query: str) -> str:
  engine = DuckDuckGoSearchResults()
  return engine.run(f"site:scholar.google.com OR site:arxiv.org OR site:ieeexplore.ieee.org OR site:researchgate.net {query}")

tool_search_web = {
  'type':'function', 
  'function':{
    'name': 'search_web',
    'description': 'Search the web and return the papers with the link to it',
    'parameters': {
            'type': 'object',
            'required': ['query'],
            'properties': {
                'query': {'type':'str', 'description':'the topic or subject to search on the web'},
            }
        }
    }
}