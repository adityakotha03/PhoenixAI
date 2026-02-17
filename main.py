from phoenix.tools.tools import Tools
from phoenix.tools.url_fetch import FetchURLContent
from phoenix.tools.memory import ReadMemory, WriteMemory
from phoenix.agent.loop_openai import OpenAILoop
from phoenix.agent.subagent import SubAgent

tools = Tools()
tools.add_tool(FetchURLContent)
tools.add_tool(ReadMemory)
tools.add_tool(WriteMemory)

LLM = OpenAILoop(model_name="gpt-5", max_completion_tokens=2048, tool_registry=tools, max_loop=5)
LLM.load_client()

# task = "Fetch content from https://haipeng-luo.net/ and Add a memory that user likes San Frasisco and Bay Area"
# task = "Add a memory that user likes Biriyani and Curry"
task = "Read the memory and tell me what the user likes"
# task = "I am currently in California, where would you suggest I travel and what food should I try?"

subagent = SubAgent(task, llm=LLM)
llm_agent = subagent.run_subagent()
print(llm_agent)
print(LLM.chat)