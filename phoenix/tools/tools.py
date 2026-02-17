from typing import Callable, Any, Type

class Tools:
    def __init__(self):
        self.tools: list[dict] = []
        self.registry: dict[str, Callable[..., Any]] = {}

    def add_tool(self, tool_cls: Type[Any]):
        definition = tool_cls.get_definition()
        name = definition["function"]["name"]

        self.tools.append(definition)
        self.registry[name] = tool_cls

    def get_tools(self) -> list[dict]:
        return self.tools

    def get_function(self, name: str) -> Callable[..., Any] | None:
        return self.registry.get(name)