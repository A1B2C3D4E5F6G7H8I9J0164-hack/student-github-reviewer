from fastapi import FastAPI
from pydantic import BaseModel
from agent.graph import github_reviewer_app

app = FastAPI()

@app.get("/")
def home():
    return {"message": "GitHub Reviewer backend is running perfectly!"}

@app.post("/review")
def review_portfolio(username: str):
    # 1. Create the starting point for our agents
    initial_state = {"username": username}
    
    # 2. Tell the LangGraph brain to start thinking!
    result = github_reviewer_app.invoke(initial_state)
    
    # 3. Return the AI's final answer
    return {
        "username": result["username"],
        "extracted_data": result.get("github_data"),
        "mentor_feedback": result.get("feedback")
    }
