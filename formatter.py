generate_format = {
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "A response content based on defined prompt."
    },
    "tool_calls": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "function": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string"
              },
              "arguments": {
                "type": "object",
                "additionalProperties": True
              }
            },
            "required": ["name", "arguments"]
          }
        },
        "required": ["function"]
      },
      "default": None
    }
  },
  "required": ["content"]
}
