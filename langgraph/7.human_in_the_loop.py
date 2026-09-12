from langgraph.graph import StateGraph, START
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langgraph.types import interrupt, Command
from dotenv import load_dotenv

load_dotenv()

# -------------------
# 1. LLM
# -------------------
# llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

# -------------------
# 2. TOOL (HITL)
# -------------------
@tool
def send_email(to: str, subject: str, body: str) -> dict:
    """
    Send an email. Requires human approval before sending.
    """

    decision = interrupt(
        f"Do you approve sending this email?\n\nTo: {to}\nSubject: {subject}\nBody: {body}\n\nType 'yes' to approve."
    )

    if decision.lower() == "yes":
        return {
            "status": "sent",
            "message": f"Email successfully sent to {to}!"
        }
    else:
        return {
            "status": "cancelled",
            "message": "Email sending was cancelled by human."
        }


tools = [send_email]
llm_with_tools = llm.bind_tools(tools)

# -------------------
# 3. STATE
# -------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# -------------------
# 4. NODES
# -------------------
def chat_node(state: ChatState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)

# -------------------
# 5. GRAPH
# -------------------
memory = MemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer=memory)

# -------------------
# 6. CLI LOOP (HITL)
# -------------------
if __name__ == "__main__":
    thread_id = "email-thread"

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        state = {"messages": [HumanMessage(content=user_input)]}

        result = chatbot.invoke(
            state,
            config={"configurable": {"thread_id": thread_id}},
        )

        # Check for interrupt
        interrupts = result.get("__interrupt__", [])

        if interrupts:
            prompt = interrupts[0].value
            print("\n=== HUMAN APPROVAL REQUIRED ===")
            print(prompt)
            decision = input("Your decision: ")

            # Resume graph
            result = chatbot.invoke(
                Command(resume=decision),
                config={"configurable": {"thread_id": thread_id}},
            )

        last_msg = result["messages"][-1]
        print("Bot:", last_msg.content, "\n")
