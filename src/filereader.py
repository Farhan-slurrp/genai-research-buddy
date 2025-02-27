import os

def read_file(path: str, is_relative: bool = False) -> str:
    if is_relative:
        path = os.path.abspath(path)
    
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file at {path} does not exist.")
    
    with open(path, 'rb') as file:
        content = file.read()
    
    return content

tool_read_file = {
  'type':'function', 
  'function':{
    'name': 'read_file',
    'description': 'Read the content of a file in the path',
    'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'Path to the file',
                },
                'is_relative': {
                    'type': 'boolean',
                    'description': 'Boolean identifier to know whether is path is relative or not',
                },
            },
            'required': ['path'],
        },
    }
}