"""
Utility wrapper to initialize Trustcall extractors for memory updates.
"""

from langchain_core.runnables import Runnable
from trustcall import create_extractor as core_create_extractor

def create_extractor(llm, tools, tool_choice, enable_inserts=False) -> Runnable:
    """
    Create a Trustcall extractor instance.

    Args:
        llm: The language model instance to use for extraction.
        tools: A list of Pydantic schemas used for extraction.
        tool_choice: Name of the tool to focus extraction on.
        enable_inserts (bool): Whether to allow insertions of new memory docs.

    Returns:
        A configured runnable Trustcall extractor.
    """
    return core_create_extractor(
        llm=llm,
        tools=tools,
        tool_choice=tool_choice,
        enable_inserts=enable_inserts
    )
