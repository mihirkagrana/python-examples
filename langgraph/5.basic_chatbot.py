from langgraph.graph import StateGraph, START, END 
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages # add_messages is a reducer which is specially optimized to store BaseMessage
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
#from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


load_dotenv()
# define state 
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

# llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)

    return {'messages': [response]}


graph = StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

# ---------- FOR IN MEMORY CHECKPOINT ---------------
# checkpointer = InMemorySaver()
# thread_id = 1
# config = {"configurable":{"thread_id": thread_id}}

# workflow = graph.compile(checkpointer=checkpointer)

# ---------- FOR SQLITE CHECKPOINT ----------
connection = sqlite3.connect(database='chatbot.db',check_same_thread=False) # check_same_thread=False says that we are using multiple threads to access sqlite 
checkpointer = SqliteSaver(conn=connection)

thread_id = 1
config = {"configurable":{"thread_id": thread_id}}

workflow = graph.compile(checkpointer=checkpointer)



while True:
    user_input = input("\n Ask anything: ")

    if user_input.strip().lower() in ['bye','exit']:
        break
    user_message = HumanMessage(content=user_input)
    initial_state = {
        'messages': [user_message]
    }


    # response = workflow.invoke(initial_state,config=config) # when you invoke again and again the state will start from scratch, thus previous data will be lost 
    # print(response['messages'][-1].content)

    # apply streaming 
    for message_chunk, metadata in workflow.stream(
        initial_state,
        config=config,
        stream_mode='messages'
    ):
        if message_chunk.content:
            print(message_chunk.content, end=" ", flush=True)

    
