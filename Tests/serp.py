import os
import requests
import json
from bs4 import BeautifulSoup

from dotenv import load_dotenv


# Load API keys from environment variables
load_dotenv()
SERPER_API_KEY = os.getenv("SERP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
        print(response.status_code)
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
    full_text = []
    for article in articles:
        # Append the heading and the fetched article content
        full_text.append(f"Title: {article['heading']}")
        article_content = fetch_article_content(article['url'])
        full_text.append(article_content)
    
    return "\n\n".join(full_text)

def test_full_process(query):
    """
    Takes a query, retrieves articles, fetches content from the top 3 articles,
    concatenates the content, and returns the final text.
    """
    # Step 1: Search for articles using the query
    articles = search_articles(query)
    
    if not articles:
        print("No articles found.")
        return None
    
    # Step 2: Limit to top 3 articles
    top_articles = articles[:3]
    print(f"Found {len(top_articles)} articles. Fetching content from top 3 articles...")

    # Step 3: Fetch content for each article in the top 3
    for index, article in enumerate(top_articles):
        print(f"Fetching content for article {index + 1}: {article['url']}")
        content = fetch_article_content(article['url'])
        
        # Save the fetched content back into the article
        article['content'] = content if content else "No content fetched."
    
    # Step 4: Concatenate the fetched content
    final_text = concatenate_content(top_articles)
    
    if final_text:
        print("Final concatenated content:\n")
        return final_text
    else:
        print("No content fetched.")
        return None


# Example usage
query = "latest AI advancements"
final_content = test_full_process(query)

if final_content:
    print(final_content)
else:
    print("Test failed to retrieve and process content.")

