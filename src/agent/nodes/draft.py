from langchain_core.messages import HumanMessage
from agent.state import State
from agent.prompts import draft_prompt
from agent.utils import call_llm

MOCK_RESPONSE = False  # Toggle to False for API calls

def generate_draft(state: State) -> State:
    """Generate a draft response based on ticket and context.
    
    Args:
        state (State): Current state with ticket, category, and context.
        
    Returns:
        State: Updated state with draft response and messages.
    """
    
    ticket = state["ticket"]
    category = state["category"]
    context = state["context"]
    
    message = draft_prompt.format(
        subject=ticket["subject"],
        description=ticket["description"],
        category=category,
        context=context
    )
    
    mock_response = (
        "Hello Customer,\n\n"
        "Thank you for contacting IT Support. It seems you are experiencing a system-related issue. "
        "Please try restarting your computer to clear any temporary system errors. "
        "If the problem persists, check for pending operating system updates and install them. "
        "You may also want to run a quick diagnostic by opening the system health tool "
        "and reviewing any flagged items.\n\n"
        "If these steps do not resolve the issue, please let us know so we can arrange a remote session "
        "for further investigation.\n\n"
        "Best regards,\nIT Support Team"
    ) if MOCK_RESPONSE else None

    
    response = call_llm(
        message=message,
        mock_response=mock_response,
        max_tokens=400,
        temperature=0.3
    )
    
    messages = state["messages"] + [HumanMessage(content=f"Draft response generated: {response}")]
    return {
        "draft": response,
        "messages": messages
    }