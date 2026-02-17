import re
import json
from typing import Any
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
except ImportError:
    pass

_TOOL_CALL_RE = re.compile(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", re.DOTALL)

def extract_tool_calls(text: str) -> list[dict[str, Any]]:
    calls = []
    for m in _TOOL_CALL_RE.finditer(text):
        try:
            calls.append(json.loads(m.group(1)))
        except json.JSONDecodeError:
            pass
    return calls

def strip_tool_calls(text: str) -> str:
    return _TOOL_CALL_RE.sub("", text).strip()

class LLMLoop:
  """Resuable class to load and generate outputs using provided LLM model"""
  def __init__(self, model_name: str, max_tokens: int = 16384, chat: list | None = None, tool_registry=None):
    self.model_name = model_name
    self.max_tokens = max_tokens
    self.chat = chat
    self.tool_registry = tool_registry
    self.tokenizer = None
    self.model = None

  def load_model(self):
    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
    self.model = AutoModelForCausalLM.from_pretrained(
        self.model_name,
        torch_dtype="auto",
        device_map="auto"
    )

  def generate(self):
    tools = self.tool_registry.get_tools() if self.tool_registry else None
    text = self.tokenizer.apply_chat_template(self.chat, tools=tools, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
    generated_ids = self.model.generate(**model_inputs, max_new_tokens=self.max_tokens)
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    content = self.tokenizer.decode(output_ids, skip_special_tokens=True)
    return content

  def run(self):
    if self.tokenizer is None or self.model is None:
      self.load_model()

    max_iters = 3
    for _ in range(max_iters):
            output = self.generate()
            calls = extract_tool_calls(output)
            assistant_text = strip_tool_calls(output)
            if assistant_text:
                self.chat.append({"role": "assistant", "content": assistant_text})
                final_text = assistant_text

            if not calls:
                return final_text or output

            for call in calls:
              name = call.get("name")
              args = call.get("arguments", {}) or {}

              tool_cls = self.tool_registry.get_function(name) if self.tool_registry else None
              if tool_cls is None:
                  tool_result = {"error": f"Unknown tool: {name}"}
              else:
                  try:
                      tool_result = tool_cls(**args).run()
                  except TypeError as e:
                      tool_result = {"error": f"Bad arguments for {name}: {e}"}
                  except Exception as e:
                      tool_result = {"error": str(e)}

              self.chat.append({
                  "role": "tool",
                  "name": name,
                  "content": json.dumps(tool_result, ensure_ascii=False)
              })

    return self.generate()