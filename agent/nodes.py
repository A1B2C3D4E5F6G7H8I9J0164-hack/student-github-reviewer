import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from .state import ReviewState

load_dotenv()

# Set up LLM
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)


def extract_github_data(state: ReviewState):
    username = state["username"]
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {github_token}"} if github_token else {}

    try:
        user_url = f"https://api.github.com/users/{username}"
        repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=5"

        user_resp = requests.get(user_url, headers=headers)
        repos_resp = requests.get(repos_url, headers=headers)

        if user_resp.status_code == 200 and repos_resp.status_code == 200:
            repos_data = repos_resp.json()

            repo_names = [repo["name"] for repo in repos_data]
            languages = list(set(
                repo["language"] for repo in repos_data if repo["language"]
            ))

            real_data = {
                "recent_repos": repo_names,
                "primary_languages": languages,
                "public_repos_count": user_resp.json().get("public_repos", 0)
            }

            return {"github_data": real_data}

        else:
            return {"github_data": {"error": f"API Error: User {username} not found."}}

    except Exception as e:
        return {"github_data": {"error": str(e)}}


def code_mentor_review(state: ReviewState):
    username = state["username"]
    data = state["github_data"]

    prompt = f"""
You are an encouraging Code Mentor. Review this GitHub portfolio data for '{username}'.

Data: {data}

Write a short, professional review. Highlight strengths based on languages,
and suggest 1–2 actionable improvements (like docs or tests).
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {"feedback": response.content}
