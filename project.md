# Mural Event Storming Tool

## Goal
Post event storming outputs (commands, events, aggregates, read models, etc.) as coloured sticky notes at specific positions on a MURAL board.

## Architecture
- Python script using `requests` to call the MURAL REST API
- Config via environment variables (`MURAL_TOKEN`, `MURAL_ID`)
- Build up from a single sticky to a full event storm layout

---

## Implementation Slices

### Slice 1 – Post a single sticky note
- POST one sticky with user-specified text to a hardcoded position
- Validate it appears on the board
- **Test:** Run script, confirm sticky visible on board

### Slice 2 – Post a sticky at a specified position
- Accept x, y coordinates as parameters
- **Test:** Post two stickies at different positions, confirm placement

### Slice 3 – Post a sticky with a specified colour
- Accept colour parameter (map event storming colours: orange=event, blue=command, yellow=aggregate, green=read model, purple=policy, pink=external system)
- **Test:** Post stickies of different colours, confirm on board

### Slice 4 – Post multiple stickies in a single run
- Accept a list of stickies (text, x, y, colour) and post them in sequence
- **Test:** Post 3+ stickies in one invocation

### Slice 5 – Event storm layout engine
- Define an event storm schema (JSON/YAML) with swim lanes or timeline positions
- Auto-calculate x, y positions based on sequence order and type
- **Test:** Feed a small event storm (3-5 steps), confirm correct layout on board

### Slice 6 – Batch optimisation
- Investigate MURAL bulk/batch endpoints to reduce API calls
- Add rate limiting/retry logic if needed
- **Test:** Post a 20+ item event storm without failures

---

## Event Storming Colour Map (DDD conventions)
| Type            | Colour  |
|-----------------|---------|
| Domain Event    | Orange  |
| Command         | Blue    |
| Aggregate       | Yellow  |
| Read Model      | Green   |
| Policy          | Purple  |
| External System | Pink    |

---

## Config
```
MURAL_TOKEN=<your-api-token>
MURAL_ID=<target-mural-board-id>
```

## Run (target for Slice 1)
```bash
python post_sticky.py "Something happened"
```
