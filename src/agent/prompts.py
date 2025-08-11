from langchain.prompts import PromptTemplate

# Classification prompt
classify_prompt = PromptTemplate.from_template("""
Classify the IT support ticket into one of: [System, Network, Settings, General]
Subject: {subject}
Description: {description}
Respond ONLY with the category name (e.g., System).
""")

# Draft generation prompt
draft_prompt = PromptTemplate.from_template("""
You are an IT helpdesk agent. Generate a concise, professional response to the customer based on the ticket and provided knowledge base context. Ensure the response:
1. Starts with a polite, personal greeting (e.g., 'Hello Customer').
2. Addresses the issue directly with clear, actionable troubleshooting steps from the context (e.g., checking connections, updating drivers, adjusting settings).
3. Ends with a professional closing (e.g., 'Best regards, IT Support Team').
4. Is concise, under 300 words, avoiding repetition or unnecessary details.
5. Avoids placeholders like '[Customer]' and uses 'Customer' or a generic term.

Ticket Subject: {subject}
Ticket Description: {description}
Category: {category}
Knowledge Base Context: {context}

Response:
""")

# Review prompt
review_prompt = PromptTemplate.from_template("""
You are a senior IT support agent. Review the draft response for:
1. Relevance: Does it address the ticket's issue and match the category (System, Network, Settings, General)?
2. Completeness: Does it include actionable troubleshooting steps from the context and a professional closing?
3. Professionalism: Is the tone polite, professional, and does it start with a personal greeting?

Return 'Approved' if the draft is relevant, mostly complete (minor issues like slight verbosity are acceptable), and professional.
Return 'Escalate' only if the draft is irrelevant, significantly incomplete (e.g., missing key troubleshooting steps or closing), or unprofessional.

If escalating, provide specific, concise feedback on what to improve (e.g., 'Add network reset steps', 'Include a closing', 'Simplify instructions').

Ticket Subject: {subject}
Ticket Description: {description}
Category: {category}
Knowledge Base Context: {context}
Draft Response: {draft}

Response: [Approved or Escalate]
Feedback (if Escalate): [specific feedback]
""")

# Feedback prompt
feedback_prompt = PromptTemplate.from_template("""
You are a senior IT support agent. The draft response was rejected. Provide concise, specific feedback on why the draft is not suitable (e.g., irrelevant, missing key troubleshooting steps, unprofessional) and suggest improvements (e.g., 'Add driver update instructions', 'Include a professional closing').

Ticket Subject: {subject}
Ticket Description: {description}
Category: {category}
Knowledge Base Context: {context}
Draft Response: {draft}

Feedback:
""")
