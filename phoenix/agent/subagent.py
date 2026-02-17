from typing import Optional
from phoenix.agent.loop import LLMLoop

class SubAgent:
    """Create a subagent to autonomously finish smaller subtasks."""

    def __init__(self, task_info: str = "", llm: Optional["LLMLoop"] = None):
        self.task_info = task_info
        self.task_done = False
        self.llm = llm

    def create_context(self):
        prompt = (
            f"You have been given the following task info: {self.task_info}. "
            "Try to execute the provided task by using all the tools available to you."
        )
        messages = [
            {"role": "system", "content": "You are a subagent that only does what's provided to you and nothing else!"},
            {"role": "user", "content": prompt},
        ]
        return messages

    def run_subagent(self):
        context = self.create_context()
        if self.llm is None:
            self.llm = LLMLoop(
                model_name="Qwen/Qwen3-4B-Instruct-2507",
                chat=context,
            )
        else:
            self.llm.chat = context
        return self.llm.run()