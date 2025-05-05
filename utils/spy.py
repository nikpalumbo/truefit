"""
Spy class to inspect and collect tool calls made during LLM execution.
"""

class Spy:
    def __init__(self):
        # Initialize an empty list to store captured tool call data
        self.called_tools = []

    def __call__(self, run):
        # Traverse the tree of execution runs and collect tool calls from chat model outputs
        queue = [run]  # Initialize queue with the root run
        while queue:
            current_run = queue.pop()  # Process each run node
            if current_run.child_runs:
                # If there are nested runs, add them to the queue for later processing
                queue.extend(current_run.child_runs)
            if current_run.run_type == "chat_model":
                # Extract the tool call output from chat model generation
                self.called_tools.append(
                    current_run.outputs["generations"][0][0]["message"]["kwargs"]["tool_calls"]
                )
