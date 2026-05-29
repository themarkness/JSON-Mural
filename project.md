# Mural Event Storming Tool

## Goal
Post event storming outputs (commands, events, actors, read models, etc.) as coloured sticky notes at specific positions on a MURAL board.

## Architecture
- Python CLI using `requests_oauthlib` to call the MURAL REST API
- OAuth2 auth flow with token caching
- Config via `.env` (client ID, secret, mural ID)
- JSON-driven layout engine for positioning stickies

---

## Implemented Features

### Post a single sticky note
- POST one sticky with user-specified text, position, and colour
- CLI: `python post_sticky.py "text" --x 100 --y 200 --colour event`

### Post multiple stickies from JSON
- Accept a JSON file with an array of stickies (text, x, y, colour)
- CLI: `python post_sticky.py --file stickies.json`

### Event storm layout engine
- JSON schema with typed stickies (event, command, actor, readmodel, policy, system, hotspot)
- Auto-calculates x, y positions based on type and sequence order
- Swim lane layout: shared timeline row for readmodel/command/event, separate rows for actor/policy/system
- Explicit column positioning with `"column": N`
- Hotspots placed ad hoc with explicit x, y

### Legend posting
- Auto-posts a colour-coded legend to the board from `legend.json`

### OAuth2 authentication
- Browser-based OAuth2 flow on first run
- Token persistence in `.token.json` with automatic reuse

### Rate limiting & retry
- Configurable delay between API calls
- Automatic retry on 429 responses with Retry-After header

---

## Future Development Ideas

### Doc-to-JSON converter
- Script to parse a structured document (Google Doc, Markdown, plain text) into the event storm JSON format
- Could use headings/sections to identify sticky types
- LLM-assisted extraction from unstructured notes

### Alternative map types
- **Story Map** — user activities across the top, stories grouped by priority below
- **Customer Journey Map** — phases as columns, touchpoints/emotions/pain points as rows
- **Wardley Map** — value chain on y-axis, evolution on x-axis
- **Impact Map** — goal → actors → impacts → deliverables as a tree layout

### Batch optimisation
- Investigate MURAL bulk/batch endpoints to reduce API calls
- Parallel posting where rate limits allow

### Board management
- Clear/reset a board before posting
- List existing stickies on a board
- Update or move existing stickies

### Templates
- Pre-built JSON templates for common event storm patterns
- Interactive CLI wizard to build an event storm step-by-step

### Export
- Read stickies from a board and export back to JSON
- Round-trip editing: pull → modify → push
