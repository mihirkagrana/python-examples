from agents import Agent, Runner 
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv

load_dotenv()

joke_agent = Agent(
    name="Streaming Agent",
    instructions="Your are a funny assistant whose main purpose is to turn serious topics into jokes, and a detailed joke",
    model="gpt-4o-mini"
)


async def main():
   result = Runner.run_streamed(joke_agent, "Tell me a joke about the political parties")
   async for event in result.stream_events():
         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
              print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())              