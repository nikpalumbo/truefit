"""
Main node that coordinates the flow based on memory and chat history.
"""

from langchain_core.messages import SystemMessage
from configuration import Configuration
from assistant_instructions import assistant_instructions
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0)

from langchain_core.messages import merge_message_runs
from models.schemas import UpdateMemory


def main_node(state, config, store):
    # Extract user ID from config
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id

    # Load profile memory
    profile_ns = ("profile", user_id)
    profile = store.search(profile_ns)
    user_profile = profile[0].value if profile else None

    # Load company memory
    company_ns = ("company", user_id)
    companies = store.search(company_ns)
    company_info = "\n".join(f"{mem.value}" for mem in companies)

    # Format assistant system prompt
    system_msg = assistant_instructions.format(profile=user_profile, company=company_info)
    
    # Generate assistant response using model and UpdateMemory tool
    response = model.bind_tools([UpdateMemory], parallel_tool_calls=False).invoke(
        [SystemMessage(content=system_msg)] + state["messages"]
    )

    return {"messages": [response]}
