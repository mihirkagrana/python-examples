import asyncio
import json
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import Client, StdioServerParameters


BASE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(BASE_DIR)
SERVER_FILE = os.path.join(BASE_DIR, "server.py")

load_dotenv()


def extract_text(response):
    if getattr(response, "text", None):
        return response.text

    for candidate in getattr(response, "candidates", []) or []:
        for part in getattr(candidate.content, "parts", []) or []:
            if getattr(part, "text", None):
                return part.text

    return ""


def extract_function_calls(response):
    tool_calls = []

    for candidate in getattr(response, "candidates", []) or []:
        for part in getattr(candidate.content, "parts", []) or []:
            if getattr(part, "function_call", None):
                tool_calls.append(part.function_call)

    return tool_calls


async def main():
    load_dotenv(os.path.join(PROJECT_DIR, ".env"))

    # Cloud-hosted MCP server
    # StreamableHttpParameters(
    #     url="https://example.com/mcp",
    #     headers={
    #         "Authorization": f"Bearer {os.environ['CLOUD_MCP_API_KEY']}",
    #     },
    # ),
    server = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_FILE],
        cwd=PROJECT_DIR,
    )

    async with Client(server) as mcp_client:
        tools_result = await mcp_client.list_tools()
        mcp_tools = tools_result.tools
        print("MCP version:", mcp_client.protocol_version)
        print("Available tools:", [tool.name for tool in mcp_tools])
        print("tool description:", [tool.description for tool in mcp_tools])
        print("parameters:", [tool.input_schema for tool in mcp_tools])

        gemini_function_declarations = [
            types.FunctionDeclaration(
                name=tool.name,
                description=tool.description or "",
                parameters=tool.input_schema,
            )
            for tool in mcp_tools
        ]

        categories_result = await mcp_client.read_resource("expense://categories")
        categories = categories_result.contents[0].text

        prompt = (
            "Add an expense of 15.75 for food on 2024-06-15 "
            "and then list all expenses between 2024-06-01 and 2024-06-30."
        )

        instructions = (
            "You are a monthly billing assistant. Use the tools to complete the request. "
            f"These are the available categories: {categories}"
        )

        gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        config = types.GenerateContentConfig(
            system_instruction=instructions,
            tools=[types.Tool(function_declarations=gemini_function_declarations)],
        )

        response = await gemini_client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=config,
        )

        while True:
            tool_calls = extract_function_calls(response)

            if not tool_calls:
                print("\nFinal response:\n")
                print(extract_text(response))
                return

            tool_outputs = []

            for call in tool_calls:
                arguments = call.args or {}
                print(f"\nRunning {call.name} with {arguments}")
                result = await mcp_client.call_tool(call.name, arguments)
                result_items = [json.loads(item.text) for item in result.content]
                output = json.dumps(result_items)
                print("Tool result:", output)
                tool_outputs.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result_items},
                    )
                )

            response = await gemini_client.aio.models.generate_content(
                model="gemini-3.6-flash",
                contents=[prompt, response.candidates[0].content, *tool_outputs],
                config=config,
            )


if __name__ == "__main__":
    asyncio.run(main())
