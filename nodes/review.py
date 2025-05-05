"""
Handles review of the generated cover letter against user profile and company details.
"""

import json
from configuration import Configuration
from langchain_anthropic import ChatAnthropic

# Initialize Claude model
claude_model = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    temperature=0,
)

def review_cover_letter(state, config, store):
    # Extract user ID from configuration
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id

    # Load user profile from memory store
    profile_namespace = ("profile", user_id)
    profile_memories = store.search(profile_namespace)
    profile = profile_memories[0].value if profile_memories else {}

    # Load company info from memory store
    company_namespace = ("company", user_id)
    company_memories = store.search(company_namespace)
    company = company_memories[0].value if company_memories else {}

    # Extract tool_call_id for LangGraph tool message
    tool_calls = state['messages'][-1].tool_calls
    tool_call_id = tool_calls[0]['id'] if tool_calls else "unknown"

    # Handle missing cover letter
    cover_letter = company.get('cover_letter')
    if not cover_letter:
        return {
            "messages": [{
                "role": "tool",
                "content": "No cover letter found to review.",
                "tool_call_id": tool_call_id
            }]
        }

    # Build the prompt for review
    prompt = f"""
You are a cover letter reviewer assistant.

Please review the following cover letter, matching it against the user's profile and the company's mission, values, and job description.

Identify:
- Strengths
- Gaps
- Matching Score (0%-100%)
- Suggestions

--- USER PROFILE ---
{json.dumps(profile, indent=2)}

--- COMPANY INFO ---
{json.dumps(company, indent=2)}

--- COVER LETTER ---
{cover_letter}
"""

    # Call Claude with the review task
    claude_response = claude_model.invoke(prompt).content

    # Return review summary as tool message
    return {
        "messages": [{
            "role": "tool",
            "content": claude_response,
            "tool_call_id": tool_call_id
        }]
    }