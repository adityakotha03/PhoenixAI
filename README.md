# PhoenixAI Personal AI Assistant

A personal AI assistant framework with tool calling capabilities, supporting both local LLM models and OpenAI's GPT models.

## Features

- Tool-based agent system for extensible functionality
- Support for local models (via Transformers) and OpenAI models
- Memory management system for persistent storage
- URL content fetching capabilities
- Async subagent execution

## Requirements

- Python 3.11 or higher
- OpenAI API key (for OpenAI-powered agents)

## Installation

1. Clone the repository

2. Install dependencies:

```bash
pip install -r requirements_discord.txt
```

3. Configure environment variables:

Create a `.env` file in the project root with the following:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Basic Agent Usage

```python
from pheonix.tools.tools import Tools
from pheonix.tools.memory import ReadMemory, WriteMemory
from pheonix.agent.loop_openai import OpenAILoop
from pheonix.agent.subagent import SubAgent

# Setup tools
tools = Tools()
tools.add_tool(ReadMemory)
tools.add_tool(WriteMemory)

# Create agent
llm = OpenAILoop(
    model_name="gpt-5",
    max_completion_tokens=2048,
    tool_registry=tools
)
llm.load_client()

# Run a task
task = "Add a memory that I like Python programming"
subagent = SubAgent(task, llm=llm)
result = subagent.run_subagent()
print(result)
```

## Project Structure

```
PersonalAI/
├── pheonix/
│   ├── agent/
│   │   ├── loop.py              # Local model agent loop
│   │   ├── loop_openai.py       # OpenAI agent loop
│   │   └── subagent.py          # Subagent wrapper
│   └── tools/
│       ├── tools.py             # Tool registry
│       ├── memory.py            # Memory read/write tools
│       └── url_fetch.py         # URL fetching tool
├── main.py                      # Example usage
├── memory.md                    # Persistent memory storage
└── .env                         # Environment configuration
```

## Available Tools

- **ReadMemory**: Read from persistent memory storage
- **WriteMemory**: Append content to persistent memory
- **FetchURLContent**: Fetch and return content from URLs

## Adding Custom Tools

1. Create a new tool class:

```python
class MyCustomTool:
    def __init__(self, param1: str):
        self.param1 = param1
    
    def run(self):
        # Your tool logic here
        return {"status": "ok", "result": "..."}
    
    @staticmethod
    def get_definition() -> dict:
        return {
            "type": "function",
            "function": {
                "name": "MyCustomTool",
                "description": "Description of what the tool does",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "Parameter description"
                        }
                    },
                    "required": ["param1"]
                }
            }
        }
```

2. Register the tool:

```python
tools.add_tool(MyCustomTool)
```

## License

Private project - All rights reserved