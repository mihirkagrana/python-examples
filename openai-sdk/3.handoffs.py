# Handoffs 

# A way for an agent to invoke another agent 

from dotenv import load_dotenv 
from agents import Agent, Runner, function_tool, handoff, RunContextWrapper

load_dotenv() 

def on_complex_math_handoff(ctx: RunContextWrapper[None]):
    print("Handing off to COMPLEX Math Tutor Agent...")

def on_math_handoff(ctx: RunContextWrapper[None]):
    print("Handing off to Math Tutor Agent...")

def on_english_handoff(ctx: RunContextWrapper[None]):
    print("Handing off to English Tutor Agent...")

@function_tool
def solve_complex_math_problem(problem: str) -> str:
    """A tool that solves complex math problems. The input is a string describing the problem, and the output is a string with the solution."""
    # This is a placeholder function. In a real implementation, this would use a math library or API to solve the problem.
    print(f"Solving complex math problem: {problem}")
    return f"The solution to the problem '{problem}' is 42."


complex_math_agent = Agent(
    name="Complex Math Agent",
    instructions="An agent that can solve complex math problems.",
    handoff_description="Use this agent to solve complex math problems. You can ask the student for the problem they need help with, and then provide a step-by-step solution.",
    tools=[solve_complex_math_problem],
)

math_tutor_agent = Agent(
    name="Math Tutor",
    instructions="An agent that helps students with math problems.If the math problem is complex, hand off to the Complex Math Agent.",
    handoff_description="Use this agent to help students with math problems. You can ask the student for the problem they need help with, and then provide a step-by-step solution.",
    handoffs=[handoff(complex_math_agent, on_handoff=on_complex_math_handoff)],
    tools=[],
)

english_tutor_agent = Agent(
    name="English Tutor",
    instructions="An agent that helps students with English problems.",
    handoff_description="Use this agent to help students with English problems. You can ask the student for the problem they need help with, and then provide a step-by-step solution.",
    tools=[],
)
    

main_agent = Agent(
    name="Main Agent",
    instructions="An agent that helps students with their homework. If the student has a math problem, hand off to the Math Tutor agent. If the student has an English problem, hand off to the English Tutor agent.",
    handoffs=[ handoff(math_tutor_agent, on_handoff=on_math_handoff), handoff(english_tutor_agent, on_handoff=on_english_handoff)],
)


async def main():
   response = await Runner.run(main_agent, "I need help with a Maths: What is the root of 9?")
   print(response.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())   