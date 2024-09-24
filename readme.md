# Content AI

## Overview

Content AI is a Large Language Model (LLM) application designed to provide users with contextual answers based on web content. By leveraging the Serper API, the application searches the web to gather relevant information, which is then processed and presented to users through an intuitive interface. The project comprises a Flask API as the backend service and a Streamlit-based frontend for user interaction.

You can clone and deploy this application with changes on any cloud service

## Key Features

- **Web-Powered Responses**: Utilizes the Serper API to fetch and scrape content from the internet.
- **Flask Backend**: A robust API that processes user queries and communicates with the LLM.
- **Streamlit Frontend**: A user-friendly interface for seamless interaction with the application.

## Process Overview

## Demo



https://github.com/user-attachments/assets/3be1095a-c91b-4667-aeec-184c1f0603e2


1. **User Input via Streamlit Interface**:
   - Users enter their queries in a simple and engaging Streamlit-based front end.

2. **Query Handling by Flask Backend**:
   - The input query is sent to the Flask backend via an API call for processing.

3. **Web Search and Content Retrieval**:
   - The backend uses the Serper API to search the internet and retrieve relevant articles based on the user's query.

4. **Content Processing**:
   - The fetched content is processed to extract useful information, including headings and text snippets.

5. **LLM Response Generation**:
   - The processed content, along with the user's query, is passed to the LLM to generate an informative response.

6. **Response Display**:
   - The generated answer is returned to the Streamlit interface, where it is displayed to the user.

## Prerequisites

- Python 3.8 or above

## Setup Instructions

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/your-repo-url.git
cd project_name
```

### Step 2: Set Up a Virtual Environment

Use either `venv` or `conda` to create an isolated environment for the project.

#### Using `venv`

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

#### Using `conda`

```bash
conda create --name project_env python=3.8
conda activate project_env
```

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory and add your API keys to ensure they can be accessed by the application.

### Step 5: Run the Flask Backend

Navigate to the `flask_app` directory and start the Flask server:

```bash
cd flask_app
python app.py
```

### Step 6: Run the Streamlit Frontend

In a new terminal, run the Streamlit app:

```bash
cd streamlit_app
streamlit run app.py
```

### Step 7: Open the Application

Open your web browser and navigate to `http://localhost:8501` to interact with the application.

## Project Structure

- **flask_app/**: Contains the backend Flask API and utility functions.
- **streamlit_app/**: Contains the Streamlit front-end code.
- **.env**: Stores API keys (ensure this file is excluded from version control).
- **requirements.txt**: Lists the project dependencies.

## Task Instructions for Contributors

You are encouraged to:

1. Implement functionality to fetch, process, and generate responses using the Serper API.
2. Integrate the APIs effectively within the Flask backend.
3. Ensure a smooth user experience in the Streamlit frontend.

