import os
import base64
import requests
from datetime import datetime
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware


#To run the FastAPI launch it with Uvicorn:
#   uvicorn main:app --reload  
# (main:app: main is the Python file, app is the FastAPI instance.
# --reload: Enables auto-reload during development.)

#Run on a Specific Host/Port: uvicorn main:app --host 0.0.0.0 --port 8000
# --host 0.0.0.0: Makes the server accessible from other devices on your network
# --port 8000: Specifies the port (default is 8000).

#For at køre det virtuelle miljø "venv": .\venv\Scripts\activate


# Load environment variables
load_dotenv()

# GitHub API configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")  # Your GitHub username
REPO_NAME = os.getenv("REPO_NAME")    # Your GitHub Pages repo name
BRANCH = "main"  # Or "master" if using the old default

app = FastAPI()

# Allow GitHub Pages domain to call this API
origins = [
    "https://ren3mh.github.io",  # your GitHub Pages site
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # or ["*"] for testing (not recommended long-term)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/newpost/")
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = None
):
    # Generate a filename for the post (e.g., 2025-08-21-my-post.md)
    post_date = datetime.now().strftime("%Y-%m-%d")
    post_slug = title.lower().replace(" ", "-")
    post_filename = f"_posts/{post_date}-{post_slug}.md"

    # Create the Markdown content
    markdown_content = f"""---
title: "{title}"
date: "{post_date}"
---

{content}
"""

    # Upload the post to GitHub
    try:
        # Create the Markdown file in the repo
        create_file_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{post_filename}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "message": f"Add new post: {title}",
            "content": base64.b64encode(markdown_content.encode()).decode()
        }
        response = requests.put(create_file_url, headers=headers, json=data)
        response.raise_for_status()

        # Handle image upload if provided
        if image:
            image_filename = f"images/{post_date}-{image.filename}"
            image_content = await image.read()
            image_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{image_filename}"
            image_data = {
                "message": f"Add image for post: {title}",
                "content": base64.b64encode(image_content).decode()
            }
            image_response = requests.put(image_url, headers=headers, json=image_data)
            image_response.raise_for_status()

            # Update the post with the image URL
            image_path = f"{REPO_NAME}/images/{image_filename}"
            updated_content = f"{markdown_content}\n![Image]({image_path})\n"
            update_data = {
                "message": f"Update post with image: {title}",
                "content": base64.b64encode(updated_content.encode()).decode(),
                "sha": response.json()["content"]["sha"]
            }
            requests.put(create_file_url, headers=headers, json=update_data)

        return JSONResponse(content={"message": "Indlæget blev lavet fint"})

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"GitHub API error: {e}")
