"""
generate_script.py
Sends one fetched tool to Groq's free-tier API to draft a video script.
Requires GROQ_API_KEY in the environment (see .env.example).

IMPORTANT: This produces a DRAFT only. You still need to:
  1. Actually use the tool yourself and record your screen.
  2. Fill in the [YOUR HANDS-ON NOTES] and [YOUR VERDICT] sections with your
     real findings/opinion before recording voiceover.
This step is not optional - publishing scripts with no real human testing or
opinion is exactly the pattern YouTube's inauthentic content policy flags.
"""

import os
import requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SCRIPT_PROMPT_TEMPLATE = """You are drafting a YouTube video script for a faceless AI-tools
explainer channel. The host is a consistent on-screen animated character (not a real
influencer name, not a copyrighted character) who explains AI tools in a clear,
relatable, slightly conversational tone. Avoid generic hype phrases ("game changer",
"mind blowing", "let's dive in"). Keep sentences short enough to sit comfortably under
a voiceover.

Tool name: {name}
Tagline: {tagline}
Description: {description}
Website: {website}

Write a script with these exact sections, using markdown headers:

## Hook (10-15 seconds)
A specific, concrete opening line about the problem this tool solves. No throat-clearing.

## Context (30-45 seconds)
Who this is for and what the viewer will see in the video.

## Walkthrough (leave as instructions, not content)
Write 5-7 bullet points of WHAT TO SCREEN-RECORD, in the order to show it. Do not
invent example outputs - mark each bullet as [RECORD: ...].

## Your Hands-On Notes
Write literally: "[YOUR HANDS-ON NOTES - fill in after testing the tool yourself]"

## Verdict (30-45 seconds)
Write literally: "[YOUR VERDICT - fill in your honest opinion after testing]"

## Call to action
A short, natural sub/follow prompt, not salesy.

Keep total spoken content (excluding the two placeholder sections) to about 700-900 words.
"""


def generate_script(tool: dict) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Add it as a repo secret or in your .env file.")

    model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    prompt = SCRIPT_PROMPT_TEMPLATE.format(
        name=tool["name"],
        tagline=tool["tagline"],
        description=tool["description"],
        website=tool.get("website", "N/A"),
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":
    example_tool = {
        "name": "ExampleTool",
        "tagline": "AI that does the example thing",
        "description": "A longer description of what it does.",
        "website": "https://example.com",
    }
    print(generate_script(example_tool))
