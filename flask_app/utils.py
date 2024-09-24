import os
import requests
import json
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv


# Load API keys from environment variables
load_dotenv()
SERPER_API_KEY = os.getenv("SERP_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def search_articles(query):
    """ 
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text snippets.
    """
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query,
        "gl": "in"
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    

    # Make the POST request to Serper API
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        # Parse the response and extract article data
        data = response.json()
        articles = []

        for result in data.get('organic', []):
            article = {
                'url': result.get('link'),
                'heading': result.get('title'),
                'snippet': result.get('snippet', '')
            }
            articles.append(article)
        
        return articles
    else:
        print(f"Error in searching articles: {response.status_code}, {response.text}")
        return []

def fetch_article_content(url):
    """
    Fetches the article content, extracting headings and text.
    Uses BeautifulSoup to parse the HTML of the page.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = []
            
            # Extract headings (h1, h2, h3)
            for heading in soup.find_all(['h1', 'h2', 'h3']):
                content.append(heading.get_text().strip())
            
            # Extract paragraphs
            for paragraph in soup.find_all('p'):
                content.append(paragraph.get_text().strip())
            
            return "\n".join(content)
        else:
            print(f"Failed to fetch content from {url}")
            return ""
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return ""


def concatenate_content(articles):
    """
    Concatenates the content of the provided articles into a single string.
    Each article's heading and fetched content are appended together.
    """
    content = ""
    full_text = []
    for article in articles:
        # Append the heading and the fetched article content
        full_text.append(f"Title: {article['heading']}")
        article_content = fetch_article_content(article['url'])
        full_text.append(article_content)
        content += "\n\n".join(full_text)
        print(content)
        return content

def get_system_prompt(content):
    return f"""
    You are a helpful assistant that can answer questions and assist with tasks based on provided articles.
    You have access to content retrieved from the following articles:
    
    {content}
    
    When responding, ensure your answers are:
    - Simple
    - Desctiptive
    - Long answer 
    - Accurate

    Use the information from the articles to answer the user's query effectively.
    And dont deny answers use the articles in the best possible way to give the answer 
    """

    
def get_llm_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b-exp-0827",
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
    )



def generate_answer(content, query):
    """
    Generates an answer from the concatenated content using GPT-4.
    The content and the user's query are used to generate a contextual answer.
    """
    # Create the prompt based on the content and the query
    model = get_llm_model()
    system_prompt = get_system_prompt(content)

    chat_session = model.start_chat(
        history=[{
            "role": "model",
            "parts": system_prompt
        }]
    )

    response = chat_session.send_message(query)
    return response.text

