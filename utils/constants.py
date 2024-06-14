def request_payload(query: str) -> dict:
    return  {
                "model": "gpt-4o",
                "stream": True,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful multilingual and multimodal assistant called Astra. You can analyze images and answer questions about them, and you can type responses."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "functions": [
                    {
                        "name": "analyze_image",
                        "description": "Analyze the current screen or camera image",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string",
                                    "enum": ["screen", "camera"],
                                    "description": "The source of the image to analyze"
                                }
                            },
                            "required": ["source"]
                        }
                    },
                    {
                        "name": "type_text",
                        "description": "Type the provided text",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "The text to type"
                                }
                            },
                            "required": ["text"]
                        }
                    }
                ]
            }

