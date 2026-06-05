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
- **Assumption Map** — 4-quadrant grid (x-axis: known ↔ unknown, y-axis: important ↔ unimportant). Stickies placed into quadrants: Known & Important, Unknown & Important, Known & Unimportant, Unknown & Unimportant. Prioritise testing assumptions in the Unknown & Important quadrant
- **Opportunity Solution Tree** — tree layout with desired outcome at the top, branching down into opportunities, then solutions, then experiments. Visualises how discovery work connects back to a target outcome
- **Now/Next/Later Roadmap** — 3-column layout for prioritisation without committing to dates
- **RICE/ICE Scoring Matrix** — 2×2 grid (effort vs impact) or ranked list for prioritising opportunities
- **Empathy Map** — 4-quadrant layout (Says/Thinks/Does/Feels) centred around a persona
- **Service Blueprint** — horizontal timeline with swim lane rows: customer actions, frontstage, backstage, support processes
- **Lean Canvas** — 9-box business model layout (problem, solution, key metrics, unique value prop, etc.)
- **SWOT Analysis** — 4-quadrant grid (Strengths/Weaknesses/Opportunities/Threats)

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
