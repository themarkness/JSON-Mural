# Mural Sticky Poster

A CLI tool for product teams to post stickies to a MURAL board from the command line. Useful for quickly populating boards with structured data. An included example is a process 'Event Storm'.

While the nature of event storming and many other visualisation techniques is collaborative, this tool offers a quick start, aiming to get the map on the board and let the discussion take centre stage.

## Setup

### Set up a MURAL app

1. Go to https://developers.mural.co and sign in
2. Navigate to **Your apps** → **Create new app**
3. Give it a name (e.g. "Sticky Poster CLI")
4. Set the redirect URI to exactly: `http://127.0.0.1:8000/`
5. Under scopes, enable `murals:read` and `murals:write`
6. Save the app
7. Copy the **Client ID** and **Client Secret** somewhere so you can add into your `.env` file later

### Setup the python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configure credentials

Run the interactive setup:

```bash
python setup.py
```

It will prompt for:
- **Client ID** and **Client Secret** from your MURAL app
- **Mural board URL or ID** — paste the full board URL (e.g. `https://app.mural.co/t/myworkspace/m/myworkspace/myworkspace.1780064070379/...`) and it will extract the ID automatically, or enter the ID directly (e.g. `myworkspace.1780064070379`)

Config is saved to `.env`. Setup runs automatically on first use if `.env` is missing.

## Usage

```bash
python main.py
```

You'll be prompted to choose:

1. **Post a single sticky** — specify text, position, and hex colour
2. **Post an event storm** — from a JSON file (or the included example)
3. **Generate event storm JSON** — prints an LLM prompt you can use to convert a process doc into valid JSON for this tool
4. **Re-run setup** — update credentials or board ID

## Event Storm Mode

When posting an event storm, stickies are automatically laid out in swim lanes based on their type:

### Sticky Types

| Type       | Colour | Use for                                         |
|------------|--------|-------------------------------------------------|
| `event`    | Orange | Things that happened — "Config submitted"       |
| `command`  | Blue   | Actions someone took — "Submit config"          |
| `actor`    | Yellow | Who did it — "Onboarding", "RP"                 |
| `readmodel`| Green  | Info needed to make a decision — "Checklist"    |
| `policy`   | Purple | Business rules / automated reactions            |
| `system`   | Pink   | Tools involved — "ServiceNow", "Slack"          |
| `hotspot`  | Red    | Problems / pain points — "This takes 5 days"    |

### Layout

```
Row 1 (y=0)    │ actor    │ actor    │ actor    │
Row 2 (y=200)  │ readmodel│ command  │ event    │ readmodel│ command  │ event    │ ...
Row 3 (y=400)  │ policy   │ policy   │
Row 4 (y=600)  │ system   │ system   │
```

- **readmodel, command, event** share the same row and flow left-to-right as the main timeline
- **actor, policy, system** each have their own row and flow independently
- **hotspot** is placed ad hoc with explicit `x` and `y` near the related sticky

### JSON Schema

```json
[
  {"type": "actor", "text": "Engagement Manager"},
  {"type": "readmodel", "text": "Onboarding checklist"},
  {"type": "command", "text": "Send onboarding manual"},
  {"type": "event", "text": "Manual sent to service team"},
  {"type": "policy", "text": "If incomplete - request more info"},
  {"type": "system", "text": "Google Docs"},
  {"type": "hotspot", "text": "This takes 5 days", "x": 500, "y": 300}
]
```

- Items are placed left-to-right in the order they appear
- Use `"column": N` to explicitly position a sticky at a specific column
- Hotspots require `"x"` and `"y"` fields

## Generating Event Storm JSON from a Document

Don't have your process in JSON yet? Option 3 in the CLI prints a ready-made prompt you can paste into any LLM (ChatGPT, Claude, etc.) along with your process document. The LLM will return valid JSON that works directly with this tool.

The prompt is also available at `prompts/doc_to_event_storm.md` if you want to use it outside the CLI.

## Auth

On first run, a browser window opens for MURAL OAuth login.
