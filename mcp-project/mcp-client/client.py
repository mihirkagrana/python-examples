import asyncio
import os
import json
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SERVERS = {
    "math": {
        "transport": "stdio",
        "command": os.path.join(BASE_DIR, "mcp-venv", "Scripts", "python.exe"),
        "args": [
            os.path.join(BASE_DIR, "local-server", "server.py"),
        ],
    },
}


async def main():
    # Connect to MCP servers
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()

    # Map tool name → tool object
    named_tools = {tool.name: tool for tool in tools}
    print("Available tools:", named_tools.keys())

    # # Bind tools to LLM
    # llm = ChatOpenAI(model="gpt-4o-mini")
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

    llm_with_tools = llm.bind_tools(tools)

    # # Send user prompt
    prompt = (
        "Add an expense of 10 for housing on 2024-06-01 "
        "and then list all expenses between 2024-06-01 and 2024-06-30."
    )

    messages = [HumanMessage(content=prompt)]

    # # First LLM call (LLM decides which tools to call)
    assistant_message = await llm_with_tools.ainvoke(messages)

    print("\n Assistant message with tool calls:\n",assistant_message)

    # # Add assistant message to history
    messages.append(assistant_message)
    
    # # If this is just a normal LLM response, print and exit
    if not getattr(assistant_message, "tool_calls", None):
        print("\nLLM Reply:", assistant_message.content)
        return

    # # Execute ALL tool calls returned by the LLM
    tool_messages = []

    for call in assistant_message.tool_calls:
        tool_name = call["name"]
        tool_args = call["args"]
        tool_id = call["id"]

        print(f"\n🔧 Executing tool: {tool_name} with args: {tool_args}")

        # Execute MCP tool
        result = await named_tools[tool_name].ainvoke(tool_args)

        print(f"Tool result: {result}")

        # Create ToolMessage for EACH tool_call_id
        tool_msg = ToolMessage(
            content=json.dumps(result),
            tool_call_id=tool_id,
        )

        tool_messages.append(tool_msg)

    # Append all tool messages to conversation
    messages.extend(tool_messages)

    # Final LLM call (LLM now produces the final answer)
    final_response = await llm_with_tools.ainvoke(messages)

    print("\n Final response from LLM:\n")
    print(final_response.content)


if __name__ == "__main__":
    asyncio.run(main())
