from flask import Flask, request, jsonify, redirect, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from utils import search_articles, concatenate_content, generate_answer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Swagger UI setup
SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI
API_URL = '/static/swagger.json'  # URL for the Swagger spec (local file or direct URL)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI path
    API_URL,  # Swagger spec path
    config={  # Swagger UI config
        'app_name': "LLM Search API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/query', methods=['POST'])
def query():
    """
    Handles the POST request to '/query'. Extracts the query from the request,
    processes it through the search, concatenate, and generate functions,
    and returns the generated answer.
    ---
    tags:
      - LLM Query
    parameters:
      - in: body
        name: query
        description: The query string to search for.
        schema:
          type: object
          required:
            - query
          properties:
            query:
              type: string
              example: "Latest AI developments"
    responses:
      200:
        description: Query processed successfully
        schema:
          type: object
          properties:
            query:
              type: string
              description: The query provided by the user
            answer:
              type: string
              description: The generated answer from the LLM
      400:
        description: Invalid input
      404:
        description: No articles found
      500:
        description: Internal server error
    """
    data = request.get_json()
    query_text = data.get('query')

    if not query_text:
        return jsonify({"error": "Query text is required"}), 400

    print(f"Received query: {query_text}")

    # Step 1: Search and scrape articles based on the query
    print("Step 1: Searching articles...")
    articles = search_articles(query_text)

    if not articles:
        return jsonify({"error": "No articles found"}), 404

    # Step 2: Concatenate content from the scraped articles
    print("Step 2: Concatenating content...")
    content = concatenate_content(articles[:3])  # Get content from the top 3 articles

    if not content:
        return jsonify({"error": "Failed to retrieve article content"}), 500

    # Step 3: Generate an answer using the LLM
    print("Step 3: Generating answer...")
    answer = generate_answer(content, query_text)

    return jsonify({"query": query_text, "answer": answer})

@app.route('/')
def home():
    return redirect(url_for('swagger_ui'))

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
