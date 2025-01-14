import sqlite3
from typing import Annotated, Literal, TypedDict
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from src.prompts.psycologist_prompt import PSYCOLOGIST_PROMPT

# Initialize sqlite3 DB
conn = sqlite3.connect("db/checkpoints.sqlite", check_same_thread=False)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Psycologist:
    def __init__(self, llm):
        self.model = llm
        self.checkpointer = SqliteSaver(conn)
        self.workflow = self.create_workflow()

    def create_workflow(self):
        workflow = StateGraph(State)

        workflow.add_node("telegram_agent", self.call_model)

        workflow.set_entry_point("telegram_agent")

        workflow.add_conditional_edges(
             "telegram_agent",
             self.pause_after_message,
             {
                  "end": END
             }
        )

        self.app = workflow.compile(self.checkpointer)

        return self.app
    
    def call_model(self, state: State):
            print("Calling Telegram agent")
            messages = state['messages']
            response = self.model.invoke(messages)
            return {"messages": [response]}
    
    def pause_after_message(self, state: State):
         return "end"
         
    def invoke(self, message, config):
        if len(self.app.get_state(config=config).values.get("messages", [])) == 0: # if it's the first iteration
            self.app.update_state(config, {"messages": [SystemMessage(content=PSYCOLOGIST_PROMPT)]})
        sent_message = HumanMessage(content=message)
        final_state = self.app.invoke({"messages": [sent_message]}, config=config)
        return final_state["messages"][-1].content