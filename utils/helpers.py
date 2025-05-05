"""
Helper functions for routing and tool output formatting.
"""

from typing import Literal, Dict, Any
from langgraph.graph import END


def route_message(state: Dict[str, Any]) -> Literal[END, "update_profile", "update_company", "fetch_company_info", "review_cover_letter"]:
    """
    Routes execution to the correct node based on the latest tool call in the state.
    
    Note: This function only needs the state parameter for conditional edge routing.
    The config and store parameters should not be declared here to avoid the
    'Missing required config key' error.
    """
    message = state['messages'][-1]
    if not message.tool_calls:
        return END  # If no tool calls, end the graph execution

    tool_call = message.tool_calls[0]
    update_type = tool_call['args']['update_type']

    # Map update type to the corresponding node label
    if update_type == "user":
        return "update_profile"
    elif update_type == "company":
        return "update_company"
    elif update_type == "company_info":
        return "fetch_company_info"
    elif update_type == "review":
        return "review_cover_letter"
    else:
        # Default case to handle any unexpected values
        return END


def extract_tool_info(tool_calls, schema_name="Memory"):
    """
    Parse tool call results to summarize what was extracted or patched.
    """
    changes = []

    for call_group in tool_calls:
        for call in call_group:
            if call['name'] == 'PatchDoc':
                patches = call['args'].get('patches', [])
                changes.append({
                    'type': 'update',
                    'doc_id': call['args'].get('json_doc_id', 'unknown'),
                    'planned_edits': call['args'].get('planned_edits', 'unknown'),
                    'value': patches[0]['value'] if patches else 'No patch content available'
                })
            elif call['name'] == schema_name:
                changes.append({
                    'type': 'new',
                    'value': call['args']
                })

    result_parts = []
    for change in changes:
        if change['type'] == 'update':
            result_parts.append(
                f"Document {change['doc_id']} updated:\n"
                f"Plan: {change['planned_edits']}\n"
                f"Added content: {change['value']}"
            )
        else:
            result_parts.append(
                f"New {schema_name} created:\n"
                f"Content: {change['value']}"
            )

    return "\n\n".join(result_parts)