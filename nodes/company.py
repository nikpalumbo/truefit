"""
Handles company information memory updates and enrichment from web data.
"""

import uuid
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage, merge_message_runs
from configuration import Configuration
from trustcall import create_extractor
from utils.spy import Spy
from utils.helpers import extract_tool_info
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from models.schemas import CompanyInfo

# Initialize LLM and search tool
model = ChatOpenAI(model="gpt-4o", temperature=0)
tavily_search = TavilySearchResults()

# Instruction used for Trustcall memory extraction
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

def update_company(state, config, store):
    # Extract user ID from configuration
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    namespace = ("company", user_id)

    # Retrieve existing company memory entries
    existing_items = store.search(namespace)
    tool_name = "CompanyInfo"
    existing_memories = [
        (item.key, tool_name, item.value) for item in existing_items
    ] if existing_items else None

    # Format Trustcall instruction and prepare messages
    system_msg = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    updated_messages = list(
        merge_message_runs([SystemMessage(content=system_msg)] + state["messages"][:-1])
    )

    # Spy to capture tool calls made during extraction
    spy = Spy()

    # Create extractor for company info with tool listener
    company_extractor = create_extractor(
        model, tools=[CompanyInfo], tool_choice=tool_name, enable_inserts=True
    ).with_listeners(on_end=spy)

    # Run extraction
    result = company_extractor.invoke({
        "messages": updated_messages,
        "existing": existing_memories
    })

    # Store extracted company info
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(namespace, rmeta.get("json_doc_id", str(uuid.uuid4())), r.model_dump(mode="json"))

    # Format tool response message
    tool_calls = state["messages"][-1].tool_calls
    company_update_msg = extract_tool_info(spy.called_tools, tool_name)
    return {
        "messages": [{
            "role": "tool",
            "content": company_update_msg,
            "tool_call_id": tool_calls[0]["id"]
        }]
    }

def fetch_company_info(state, config, store):
    # Extract user ID and namespace
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    namespace = ("company", user_id)

    # Retrieve company memory
    existing_items = store.search(namespace)
    tool_name = "CompanyInfo"
    existing_memories = [
        (item.key, tool_name, item.value) for item in existing_items
    ] if existing_items else None

    # Pull company name if available
    company = existing_items[0].value if existing_items else {}
    company_name = company.get("name") if company else None

    # Handle missing company name
    tool_calls = state["messages"][-1].tool_calls
    if not company_name:
        return {
            "messages": [{
                "role": "tool",
                "content": "Company name is missing. Please ask the user to provide it.",
                "tool_call_id": tool_calls[0]["id"]
            }]
        }

    # Format instruction and prepare messages
    system_msg = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    updated_messages = list(
        merge_message_runs([SystemMessage(content=system_msg)] + state["messages"][:-1])
    )

    # Perform Tavily web search if mission/values are missing
    query = f"{company_name} company mission and values"
    search_results = tavily_search.invoke({"query": query})

    # Append search content to message history
    if search_results:
        summary = "\n".join([res["content"] for res in search_results if "content" in res][:2])
        updated_messages.append(HumanMessage(content=f"Additional info from web search:\n{summary}"))

    # Spy to track tool calls made by extractor
    spy = Spy()

    # Create extractor with tool listener
    company_extractor = create_extractor(
        model, tools=[CompanyInfo], tool_choice=tool_name, enable_inserts=True
    ).with_listeners(on_end=spy)

    # Invoke extraction
    result = company_extractor.invoke({
        "messages": updated_messages,
        "existing": existing_memories
    })

    # Save updates to memory store
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(namespace, rmeta.get("json_doc_id", str(uuid.uuid4())), r.model_dump(mode="json"))

    # Return tool message describing what changed
    company_update_msg = extract_tool_info(spy.called_tools, tool_name)
    return {
        "messages": [{
            "role": "tool",
            "content": company_update_msg,
            "tool_call_id": tool_calls[0]["id"]
        }]
    }
