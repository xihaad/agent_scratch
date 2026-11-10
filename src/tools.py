import json
import os
import requests
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv(override=True)

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")

pushover_url = "https://api.pushover.net/1/messages.json"


def push(text):
    requests.post(
        pushover_url,
        data={
            "token": pushover_token,
            "user": pushover_user,
            "message": text,
        },
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK"


def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return "OK"


def web_search(query):
    try:
        results = DDGS().text(query, max_results=5)
    except Exception as e:
        return f"Web search failed: {e}"
    if not results:
        return "No results found"
    return [{"title": r["title"], "link": r["href"], "snippet": r["body"]} for r in results]


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

web_search_json = {
    "name": "web_search",
    "description": "Search the web for public information about the person you represent, such as recent projects, publications, talks or news. Use it when the answer is not in your context.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query, including the person's full name"},
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
    {"type": "function", "function": web_search_json},
]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
    "web_search": web_search,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = tool_map.get(tool_name)
        result = tool(**arguments) if tool else "Unknown tool: " + tool_name
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
