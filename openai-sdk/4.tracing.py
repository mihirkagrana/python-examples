from agents import Agent, Runner, trace
from dotenv import load_dotenv 

load_dotenv() 


agent1 = Agent(
    name="Researcher",
    instructions="Research the topic and summarize",
    model="gpt-4o-mini"
)

agent2 = Agent(
    name="Writer",
    instructions="Write a blog post from the research in 50 words or less",
    model="gpt-4o-mini"
)

async def main():
    with trace("Research Agent Trace"):
        result1 = await Runner.run(agent1, "AI agents in healthcare")

        result2 = await Runner.run(agent2, result1.final_output)

        print(result2.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())        