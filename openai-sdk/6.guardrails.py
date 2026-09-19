from agents import Agent, Runner, GuardrailFunctionOutput, RunContextWrapper, output_guardrail, input_guardrail
from pydantic import BaseModel
import re
from dotenv import load_dotenv

load_dotenv()


class FinanceAnswer(BaseModel):
    answer: str
    disclaimer: str

@input_guardrail
def finance_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input_text: str  # Note: The 3rd arg is the raw user string
) -> GuardrailFunctionOutput:
    
    print("Running input guardrail for finance agent...")
    # Block users trying to ask for "insider" info or "hacks"
    illegal_requests = [
        r"insider trading",
        r"hack the market",
        r"manipulate stock",
        r"avoid taxes illegally"
    ]

    for p in illegal_requests:
        if re.search(p, input_text.lower()):
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info="Input blocked: Request contains prohibited financial keywords."
            )

    return GuardrailFunctionOutput(
        output_info="Input passed finance compliance checks.",
        tripwire_triggered=False,
    )

@output_guardrail
def finance_compliance_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: FinanceAnswer
) -> GuardrailFunctionOutput:

    banned_patterns = [
        r"guaranteed return",
        r"risk[- ]?free",
        r"double your money",
        r"insider tip"
    ]

    for p in banned_patterns:
        if re.search(p, output.answer.lower()):
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info="Compliance violation: Prohibited financial terminology."
            )

    return GuardrailFunctionOutput(
        output_info="Output passed finance compliance checks.",
        tripwire_triggered=False,
    )

finance_agent = Agent(
    name="FinanceAdvisor",
    instructions="""
    Provide general financial education only.
    Never give personalized or guaranteed advice.
    """,
    output_type=FinanceAnswer,
    input_guardrails=[finance_input_guardrail],
    output_guardrails=[finance_compliance_guardrail],
    model="gpt-4o-mini"
)
   
import asyncio

async def main():
    try:
        result = await Runner.run(
            finance_agent,
            #"How can I get guaranteed 20 percent stock returns?"
            "Can you explain what is index funnd to me?"
        )
        print(result.final_output)
    except Exception as e:
        if "tripwire" in str(e).lower():
           print("Compliance Block: The agent's response was blocked for financial safety.")
        else:
            print(f"Technical Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())   

