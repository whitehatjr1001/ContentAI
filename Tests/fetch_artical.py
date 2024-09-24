import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json


# Load API keys from environment variables
load_dotenv('.env')

SERPER_API_KEY = os.getenv("SERP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
def parse_snippets(results):
    snippets = []

    # Check if there's an answer box
    if results.get("answerBox"):
        answer_box = results.get("answerBox", {})
        if answer_box.get("answer"):
            return [answer_box.get("answer")]
        elif answer_box.get("snippet"):
            return [answer_box.get("snippet").replace("\n", " ")]
        elif answer_box.get("snippetHighlighted"):
            return answer_box.get("snippetHighlighted")

    # Check if there's a knowledge graph
    if results.get("knowledgeGraph"):
        kg = results.get("knowledgeGraph", {})
        title = kg.get("title")
        entity_type = kg.get("type")
        if entity_type:
            snippets.append(f"{title}: {entity_type}.")
        description = kg.get("description")
        if description:
            snippets.append(description)
        for attribute, value in kg.get("attributes", {}).items():
            snippets.append(f"{title} {attribute}: {value}.")
    # Parse the organic search results (Top 3 results)
    for result in results.get("organic", [])[:3]:
        if "snippet" in result:
            snippets.append(result["snippet"])
        for attribute, value in result.get("attributes", {}).items():
            snippets.append(f"{attribute}: {value}.")
            
    if len(snippets) == 0:
        return ["No good Google Search Result was found"]
    return snippets

def fetch_top_3_results(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query,
        "gl": "in"
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    # Make the API request
    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()  # Check if request was successful
    
    # Parse the response to JSON
    search_results = response.json()

    # Extract relevant snippets from top 3 results
    top_3_snippets = parse_snippets(search_results)
    
    return top_3_snippets

# Example usage:
query = "Mark Zuckerberg"
top_3_snippets = fetch_top_3_results(query)
for snippet in top_3_snippets:
    print(snippet)


