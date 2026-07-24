"""
fetch_tools.py
Pulls recent AI/SaaS tool launches from Product Hunt's free GraphQL API.
Requires PRODUCTHUNT_TOKEN in the environment (see .env.example).
"""

import os
import json
import requests

PH_API_URL = "https://api.producthunt.com/v2/api/graphql"

QUERY = """
query TrendingAITools {
  posts(order: RANKING, first: 15, topic: "artificial-intelligence") {
    edges {
      node {
        id
        name
        tagline
        description
        url
        website
        votesCount
        topics {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}
"""


def fetch_trending_tools():
    token = os.environ.get("PRODUCTHUNT_TOKEN")
    if not token:
        raise RuntimeError("PRODUCTHUNT_TOKEN is not set. Add it as a repo secret or in your .env file.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        PH_API_URL,
        headers=headers,
        json={"query": QUERY},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    edges = data.get("data", {}).get("posts", {}).get("edges", [])
    tools = []
    for edge in edges:
        node = edge["node"]
        tools.append(
            {
                "name": node["name"],
                "tagline": node["tagline"],
                "description": node["description"],
                "url": node["url"],
                "website": node.get("website"),
                "votes": node["votesCount"],
                "topics": [t["node"]["name"] for t in node["topics"]["edges"]],
            }
        )
    # Highest-voted first
    tools.sort(key=lambda t: t["votes"], reverse=True)
    return tools


def pick_next_tool(tools, already_covered_path="output/covered_tools.json"):
    """Skip tools you've already made a video about."""
    covered = []
    if os.path.exists(already_covered_path):
        with open(already_covered_path, "r", encoding="utf-8") as f:
            covered = json.load(f)

    for tool in tools:
        if tool["name"] not in covered:
            return tool, covered
    return None, covered


if __name__ == "__main__":
    tools = fetch_trending_tools()
    print(json.dumps(tools, indent=2))
