import json
import os
from typing import Any
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


class OpenAILoop:
    """Reusable class to generate outputs using OpenAI's API with tool calling support"""
    def __init__(self, model_name: str = "gpt-5", max_completion_tokens: int = 4096, chat: list | None = None, tool_registry=None, max_loop: int = 10):
        self.model_name = model_name
        self.max_completion_tokens = max_completion_tokens
        self.chat = chat if chat else []
        self.tool_registry = tool_registry
        self.client = None
        self.max_loop = max_loop
    
    def load_client(self):
        """Initialize OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
    
    def generate(self):
        """Generate a response from OpenAI with optional tool calls"""
        tools = self.tool_registry.get_tools() if self.tool_registry else None
        
        # Prepare API call parameters
        params = {
            "model": self.model_name,
            "messages": self.chat,
            "max_completion_tokens": self.max_completion_tokens
        }

        if tools:
            params["tools"] = tools
            params["tool_choice"] = "auto"
        
        response = self.client.chat.completions.create(**params)
        return response.choices[0].message
    
    def run(self):
        """Run the agent loop with tool execution"""
        if self.client is None:
            self.load_client()
        
        for _ in range(self.max_loop):
            message = self.generate()
            if message.tool_calls:
                self.chat.append({
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })
                
                # Execute each tool call
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        function_args = {}
                    
                    tool_cls = self.tool_registry.get_function(function_name) if self.tool_registry else None
                    
                    if tool_cls is None:
                        tool_result = {"error": f"Unknown tool: {function_name}"}
                    else:
                        try:
                            tool_result = tool_cls(**function_args).run()
                        except TypeError as e:
                            tool_result = {"error": f"Bad arguments for {function_name}: {e}"}
                        except Exception as e:
                            tool_result = {"error": str(e)}
                    
                    self.chat.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(tool_result, ensure_ascii=False)
                    })
            else:
                if message.content:
                    self.chat.append({
                        "role": "assistant",
                        "content": message.content
                    })
                    return message.content
                return message.content or "No response generated"
        
        # Generate one final response when max loop is reached
        final_message = self.generate()
        if final_message.content:
            self.chat.append({
                "role": "assistant",
                "content": final_message.content
            })
        return final_message.content or "Max loop reached"
