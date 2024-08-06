from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import praw
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import asyncio

app = FastAPI()

load_dotenv()

client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = os.getenv('REDDIT_USER_AGENT')
openai_key = os.getenv('OPENAI_API_KEY')

openai_client = OpenAI(api_key=openai_key)

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

class URLItem(BaseModel):
    url: str

def fetch_comments(comment):
    """ Recursively fetch comments and their replies """
    comments_data = []
    comment_queue = comment.replies[:]

    while comment_queue:
        current_comment = comment_queue.pop(0)
        comment_data = {
            "author": str(current_comment.author),
            "body": current_comment.body,
            "score": current_comment.score,
            "replies": fetch_comments(current_comment)
        }
        comments_data.append(comment_data)
    return comments_data

def fetch_reddit_topic(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)

    data = {
        "title": submission.title,
        "author": str(submission.author),
        "score": submission.score,
        "url": submission.url,
        "comments": []
    }

    for top_level_comment in submission.comments:
        comment_data = {
            "author": str(top_level_comment.author),
            "body": top_level_comment.body,
            "score": top_level_comment.score,
            "replies": fetch_comments(top_level_comment)
        }
        data["comments"].append(comment_data)

    return data

async def generate_summary(prompt):
    stream = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    
    accumulated_text = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            accumulated_text += chunk.choices[0].delta.content
            
            if len(accumulated_text) > 100:
                yield accumulated_text
                accumulated_text = ""
            
        await asyncio.sleep(0.1)
    
    if accumulated_text:
        yield accumulated_text

@app.post("/summarize")
async def summarize_url(item: URLItem):
    reddit_data = fetch_reddit_topic(item.url)
    final_data = json.dumps(reddit_data)

    prompt = f"""
    You are provided with a JSON dataset containing a discussion about pets. Based on the data, summarize the following points:
    1. List doing the points users like, prefer, or need as features in an application focused on pets, focusing on problems that need to be solved, Please output None if None.
    2. List doing the points users don't like or hate, including things they find frustrating or want to avoid in an application, Please output None if None.
    3. List doing the potential features that could be useful for the application, inferred from the discussion which isn't listed above and is important. Please output None if None.

    Discussion data:
    {final_data}
    """
    
    return StreamingResponse(generate_summary(prompt), media_type="text/plain")
