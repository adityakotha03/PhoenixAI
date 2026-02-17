from pathlib import Path

class ReadMemory:
    """Read long-term memory stored in memory.md"""

    def __init__(self, truncate: bool = True):
        self.memory_path = Path(__file__).parent.parent.parent / "memory.md"
        self.truncate = truncate

    def run(self):
        if not self.memory_path.exists():
            self.memory_path.write_text("", encoding="utf-8")
            return {"status": "ok", "memory": ""}
        
        if self.truncate:
            memory_content = self.memory_path.read_text(encoding="utf-8")[-1000:]
        else:
            memory_content = self.memory_path.read_text(encoding="utf-8")
        
        return {"status": "ok", "memory": memory_content}

    @staticmethod
    def get_description():
        return "Read long-term memory stored in memory.md"

    @staticmethod
    def get_definition() -> dict:
        return {
            "type": "function",
            "function": {
                "name": "ReadMemory",
                "description": "Read the long-term memory stored in memory.md file.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }


class WriteMemory:
    """Append content to long-term memory stored in memory.md"""

    def __init__(self, content: str):
        self.memory_path = Path(__file__).parent.parent.parent / "memory.md"
        self.content = content

    def run(self):
        if not self.memory_path.exists():
            self.memory_path.write_text(self.content, encoding="utf-8")
        else:
            existing = self.memory_path.read_text(encoding="utf-8")
            self.memory_path.write_text(existing + "\n" + self.content, encoding="utf-8")
        
        return {"status": "ok", "message": "Memory saved successfully"}

    @staticmethod
    def get_description():
        return "Append content to long-term memory stored in memory.md"

    @staticmethod
    def get_definition() -> dict:
        return {
            "type": "function",
            "function": {
                "name": "WriteMemory",
                "description": "Append new content to the long-term memory file (memory.md).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The text content to append to memory."
                        }
                    },
                    "required": ["content"]
                }
            }
        }