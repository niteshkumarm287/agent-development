import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "game-d8160")
REGION     = os.environ.get("GCP_REGION", "global")

vertexai.init(project=PROJECT_ID, location=REGION)
model = GenerativeModel("gemini-2.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*"],  # restrict to extension only
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

class SummarizeRequest(BaseModel):
    text: str
    mode: str = "summary"   # "summary" | "bullets" | "eli5"

PROMPTS = {
    "summary": "Summarize this webpage content in 3-4 sentences. Be concise and accurate.",
    "bullets": "Extract the 5 most important points from this content as bullet points.",
    "eli5":    "Explain the main idea of this content simply, as if to a 10-year-old.",
}

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    if len(req.text) < 50:
        raise HTTPException(400, "Page content too short to summarize")

    prompt = f"""{PROMPTS.get(req.mode, PROMPTS['summary'])}

Webpage content (first 8000 chars):
{req.text[:8000]}

Return only the summary. No preamble."""

    response = model.generate_content(prompt)
    return {"summary": response.text, "mode": req.mode}

@app.get("/health")
def health():
    return {"status": "ok"}