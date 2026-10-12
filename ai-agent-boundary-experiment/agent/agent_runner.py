"""Model integration boundary; no shell or unrestricted filesystem tool is exposed.

A supplied adapter implements next_turn(messages, tools, model, temperature) and returns
{"tool_calls": [{"name": ..., "arguments": {...}}], "final": optional_string}.
Only the adapter may communicate with an authorized model API.
"""
from agent.prompts import SYSTEM
from config import MAX_STEPS

TOOLS = [
    {'name': 'read_file', 'parameters': {'path': 'string'}},
    {'name': 'list_files', 'parameters': {'path': 'string'}},
    {'name': 'write_file', 'parameters': {'path': 'string', 'content': 'string'}},
    {'name': 'external_lookup', 'parameters': {'query': 'string'}}
]

def run_agent(adapter, gateway, objective, model, temperature):
    messages = [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': objective}]
    for _ in range(MAX_STEPS):
        reply = adapter(messages=messages, tools=TOOLS, model=model, temperature=temperature)
        messages.append({'role': 'assistant', 'content': reply})
        calls = reply.get('tool_calls', [])
        for call in calls:
            result = gateway.call(call['name'], call['arguments'])
            messages.append({'role': 'tool', 'name': call['name'], 'content': result})
        if not calls and isinstance(reply.get('final'), str):
            return reply['final'], messages
    raise RuntimeError('Agent step limit exceeded')
