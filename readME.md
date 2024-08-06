# Reddit URL Summarizer

This is a streaming-based Reddit summarization application. It consists of a FastAPI backend and a Streamlit frontend.

## Project Structure

- **Frontend**: `app.py`
- **Backend**: `main.py`

## How to Run

Follow the steps below to run the application:

1. **Clone the Repository**:

    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a `.env` File**:

    Create a `.env` file in the root directory of the project and add your credentials, you can edit the existing `.env.example` and add your keys

3. **Install the Required Packages**:

    Make sure you have all the necessary packages installed. You can install them using:

    ```sh
    pip install -r requirements.txt
    ```

4. **Start the FastAPI Backend**:

    ```sh
    uvicorn main:app --reload
    ```

5. **Run the Streamlit Frontend**:

    ```sh
    streamlit run app.py
    ```

## Description

This application allows users to input a Reddit URL and get a summarized view of the discussion from the URL. It uses OpenAI's GPT-4 model to generate the summary in a streaming manner.

### Example Usage

1. Enter the Reddit URL in the Streamlit interface.
2. Click the "Summarize" button.
3. View the generated summary on the Streamlit page.

## Requirements

- Python 3.7+
- FastAPI
- Streamlit
- PRAW (Python Reddit API Wrapper)
- OpenAI


