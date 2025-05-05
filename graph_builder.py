"""
Defines the LangGraph StateGraph for the TrueFit assistant.
"""

from langgraph.graph import StateGraph, MessagesState, START, END
from configuration import Configuration
from nodes.main_node import main_node
from nodes.profile import update_profile
from nodes.company import update_company, fetch_company_info
from nodes.review import review_cover_letter

# Initialize the graph
builder = StateGraph(MessagesState, config_schema=Configuration)

# Add nodes to the graph
builder.add_node(main_node)
builder.add_node(update_profile)
builder.add_node(update_company)
builder.add_node(fetch_company_info)
builder.add_node(review_cover_letter)

# Add starting edge
builder.add_edge(START, "main_node")

# Route based on tool call type
from utils.helpers import route_message
builder.add_conditional_edges("main_node", route_message)

# Connect each handler back to main
builder.add_edge("update_profile", "main_node")
builder.add_edge("update_company", "main_node")
builder.add_edge("fetch_company_info", "main_node")
builder.add_edge("review_cover_letter", "main_node")

# Compile the graph
graph = builder.compile()