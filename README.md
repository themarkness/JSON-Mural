# Mural Event Storming Tool

Post event storming stickies to a MURAL board from a JSON file.

## Setup

### Set up a MURAL app

1. Go to https://developers.mural.co and sign in
2. Navigate to **Your apps** → **Create new app**
3. Give it a name (e.g. "Event Storm CLI")
4. Set the redirect URI to exactly: `http://127.0.0.1:8000/`
5. Under scopes, enable `murals:read` and `murals:write`
6. Save the app
7. Copy the **Client ID** and **Client Secret** somehwere so you can add into your `.env` file later

### Setup the python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


### Add Mural info to .env

Create a `.env` file:

```
MURAL_CLIENT_ID=<your-client-id>
MURAL_CLIENT_SECRET=<your-client-secret>
MURAL_ID=<your-mural-id>
```

The `MURAL_ID` is in the format `workspacename.timestamp` (e.g. `myworkspace.1780064070379`). You can find it by listing your murals via the API.

## Usage

### Post a single sticky

```bash
python post_sticky.py "Something happened" --x 100 --y 200 --colour event
```

### Post an event storm

```bash
python event_storm.py example_event_storm.json
```

## Sticky Colours

| Type       | Colour | Use for                                         |
|------------|--------|-------------------------------------------------|
| `event`    | Orange | Things that happened — "Config submitted"       |
| `command`  | Blue   | Actions someone took — "Submit config"          |
| `actor`    | Yellow | Who did it — "Onboarding", "RP"                 |
| `readmodel`| Green  | Info needed to make a decision — "Checklist"    |
| `policy`   | Purple | Business rules / automated reactions            |
| `system`   | Pink   | Tools involved — "ServiceNow", "Slack"          |
| `hotspot`  | Red    | Problems / pain points — "This takes 5 days"    |

## Layout

The event storm is laid out in horizontal rows:

```
Row 1 (y=0)    │ actor    │ actor    │ actor    │
Row 2 (y=200)  │ readmodel│ command  │ event    │ readmodel│ command  │ event    │ ...
Row 3 (y=400)  │ policy   │ policy   │
Row 4 (y=600)  │ system   │ system   │
```

- **readmodel, command, event** share the same row and flow left-to-right as the main timeline
- **actor, policy, system** each have their own row and flow independently
- **hotspot** is placed ad hoc with explicit `x` and `y` near the related sticky

## JSON Schema

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

## Auth

On first run, a browser window opens for MURAL OAuth login.