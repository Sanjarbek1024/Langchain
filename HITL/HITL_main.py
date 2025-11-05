import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from typing import TypedDict

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY topilmadi. Iltimos .env faylga qo‘shing.")

# Gemini LLM model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

# LangGraph state type
class GraphState(TypedDict):
    email_text: str
    summary: str
    approved: bool

# Initial state
state: GraphState = {
    "email_text": "",
    "summary": "",
    "approved": False
}

# Generate summary
def generate_summary(state: GraphState):
    email_text = state["email_text"]
    prompt = f"Summarize this email clearly and concisely:\n\n{email_text}"
    response = model.invoke(prompt)

    print("\n[DEBUG] Response type:", type(response))
    print("[DEBUG] Raw response:", response)

    if isinstance(response, str):
        summary = response.strip()
    elif hasattr(response, "content"):
        if isinstance(response.content, str):
            summary = response.content.strip()
        elif isinstance(response.content, list) and len(response.content) > 0:
            part = response.content[0]
            summary = getattr(part, "text", str(part)).strip()
        else:
            summary = str(response).strip()
    else:
        summary = str(response).strip()

    state["summary"] = summary
    print("\nThe summary created by Gemini:\n")
    print(summary)
    return state

# Human review
def human_review(state):
    print("\nPlease review the summary.")
    action = input("Do you approve? (a=approve, e=edit, r=reject): ").lower()
    if action == "e":
        new_summary = input("Enter the new (edited) version:\n")
        state["summary"] = new_summary
        state["approved"] = True
    elif action == "r":
        state["approved"] = False
    else:
        state["approved"] = True
    return state

# Finalize
def finalize(state):
    if state["approved"]:
        print("\nFinal approved summary:\n")
        print(state["summary"])
    else:
        print("\nSummary rejected, regenerating...")
    return state

# Graph setup
graph = StateGraph(GraphState)
graph.add_node("generate", generate_summary)
graph.add_node("review", human_review)
graph.add_node("final", finalize)
graph.add_edge("generate", "review")
graph.add_edge("review", "final")
graph.set_entry_point("generate")
graph.set_finish_point("final")
workflow = graph.compile()

# Run workflow
def run_hitl(email_text):
    state["email_text"] = email_text
    result = workflow.invoke(state)
    if not result["approved"]:
        return run_hitl(email_text)
    print("\nWorkflow completed.")
    return result

if __name__ == "__main__":
    email_text = """
    Hello team,
    Our project deadline is extended to next Friday.
    Please update the task tracker and inform the clients.
    Regards,
    Manager
    """
    run_hitl(email_text)
