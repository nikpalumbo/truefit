"""
Handles extraction and update of the user profile memory.
"""

from datetime import datetime
import uuid
from langchain_core.messages import SystemMessage, merge_message_runs
from configuration import Configuration
from trustcall import create_extractor
from models.schemas import Profile
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0)
profile_extractor = create_extractor(llm=model, tools=[Profile], tool_choice="Profile")

TRUSTCALL_INSTRUCTION = """
Reflect on the following interaction.

You MUST extract the following fields about companies if available:
- Name
- Website
- Mission
- Vision
- Values

Even if the values are mentioned quickly in a sentence (e.g., "Trust, Grow, Confidence"), they must be extracted as a list of words.

Do not invent values if they are not mentioned. Be strict but inclusive.

System Time: {time}"""

def update_profile(state, config, store):
    # Load user ID from config
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id

    # Profile memory namespace
    namespace = ("profile", user_id)
    existing_items = store.search(namespace)

    tool_name = "Profile"
    existing_memories = [
        (item.key, tool_name, item.value) for item in existing_items
    ] if existing_items else None

    # Build message history
    system_msg = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    updated_messages = list(
        merge_message_runs(messages=[SystemMessage(content=system_msg)] + state["messages"][:-1])
    )

    # Extract new profile
    result = profile_extractor.invoke({
        "messages": updated_messages,
        "existing": existing_memories
    })

    # Store updated memory
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(namespace, rmeta.get("json_doc_id", str(uuid.uuid4())), r.model_dump(mode="json"))

    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [{
            "role": "tool",
            "content": "updated profile",
            "tool_call_id": tool_calls[0]["id"]
        }]
    }