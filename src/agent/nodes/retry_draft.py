from langchain_core.messages import HumanMessage
from agent.state import State
from agent.prompts import draft_prompt
from agent.utils import call_llm

MOCK_RESPONSE = False  # Toggle to False for API calls

def retry_draft(state: State) -> State:
    """Regenerate the draft using feedback.

    Args:
        state (State): Current state with ticket, category, context, and feedbacks.
        
    Returns:
        State: Updated state with new draft response and messages.
    
    """
    
    ticket = state["ticket"]
    category = state["category"]
    context = state["context"]
    feedbacks = state["feedbacks"]
    
    message = draft_prompt.format(
        subject=ticket["subject"],
        description=ticket["description"],
        category=category,
        context=f"{context}\n\nFeedback from previous draft: {feedbacks or 'No specific feedback provided. Ensure the response is concise and actionable.'}"
    )
    
    mock_response = (
        "Hello Customer,\n\n"
        "Thank you for contacting IT Support. It appears you are experiencing a system-related problem. "
        "Please begin by restarting your computer to refresh system processes. "
        "Next, ensure your operating system is up to date by checking for and installing any pending updates. "
        "If the issue continues, run the built-in system diagnostics tool to identify potential hardware or software conflicts. "
        "Record any error codes displayed and share them with us so we can investigate further.\n\n"
        "Best regards,\nIT Support Team"
    ) if MOCK_RESPONSE else None

    
    response = call_llm(
        message=message,
        mock_response=mock_response,
        max_tokens=400,
        temperature=0.3
    )
    
    messages = state["messages"] + [HumanMessage(content=f"Retry draft generated: {response}")]
    return {
        "draft": response,
        "messages": messages
    }