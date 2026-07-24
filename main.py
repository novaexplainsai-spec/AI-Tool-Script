"""
main.py
Orchestrator: fetch trending tools -> pick one not yet covered -> draft a script
-> save it to output/scripts/ -> update the covered-tools list.

Run manually with:  python main.py
Run automatically via .github/workflows/pipeline.yml every 3 days.
"""

import os
import json
import datetime
from dotenv import load_dotenv

from fetch_tools import fetch_trending_tools, pick_next_tool
from generate_script import generate_script

load_dotenv()

OUTPUT_DIR = "output/scripts"
COVERED_PATH = "output/covered_tools.json"


def slugify(name: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tools = fetch_trending_tools()
    tool, covered = pick_next_tool(tools, COVERED_PATH)

    if tool is None:
        print("No new uncovered tools found this run. Try again next cycle.")
        return

    print(f"Drafting script for: {tool['name']}")
    script = generate_script(tool)

    today = datetime.date.today().isoformat()
    filename = f"{today}-{slugify(tool['name'])}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {tool['name']} — draft script ({today})\n\n")
        f.write(f"Source: {tool['url']}\n\n")
        f.write(f"Website: {tool.get('website', 'N/A')}\n\n")
        f.write("---\n\n")
        f.write(script)

    covered.append(tool["name"])
    with open(COVERED_PATH, "w", encoding="utf-8") as f:
        json.dump(covered, f, indent=2)

    print(f"Saved draft to {filepath}")
    print("Reminder: this is a DRAFT. Test the tool yourself, fill in your hands-on")
    print("notes and verdict, THEN record voiceover and screen capture.")


if __name__ == "__main__":
    main()
