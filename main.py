from fastapi import FastAPI
from pydantic import BaseModel
from agent.graph import github_reviewer_app

app = FastAPI()

@app.get("/")
def home():
    return {"message": "GitHub Reviewer backend is running perfectly!"}

@app.post("/review")
def review_portfolio(username: str):
    try:
        # 1. Create the starting point
        initial_state = {"username": username}
        
        # 2. Invoke the graph
        result = github_reviewer_app.invoke(initial_state)
        
        # 3. Clean up the response
        return {
            "username": result.get("username", username),
            "extracted_data": result.get("github_data", {}),
            "mentor_feedback": result.get("feedback", "No feedback generated.")
        }
    except Exception as e:
        return {
            "error": "Internal Server Error",
            "details": str(e)
        }
