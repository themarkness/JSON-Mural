# Doc-to-Event-Storm Prompt

Copy everything below the line into an LLM (ChatGPT, Claude, etc.) along with your process document.

---

You are a domain-driven design expert. Analyse the process document I provide and produce an event storm as a JSON array.

## Output format

Return ONLY a valid JSON array. Each item is an object with these fields:

- `"type"` — one of: `event`, `command`, `actor`, `readmodel`, `policy`, `system`, `hotspot`
- `"text"` — short label (max ~6 words)
- `"x"` and `"y"` — required ONLY for `hotspot` type (place near the related sticky, estimate x as column×250, y as row: 0=actor, 200=timeline, 400=policy, 600=system)
- `"column"` — optional integer to force a sticky into a specific column position

## Sticky type definitions

| Type | Meaning | Example |
|------|---------|---------|
| `event` | Something that happened (past tense) | "Order placed" |
| `command` | An action someone or something triggers | "Submit order" |
| `actor` | A person or role that issues commands | "Customer" |
| `readmodel` | Information needed to make a decision | "Product catalogue" |
| `policy` | A business rule or automated reaction ("When X, then Y") | "If payment fails, notify customer" |
| `system` | An external system or tool involved | "Stripe" |
| `hotspot` | A pain point, question, or risk | "Takes 3 days — why?" |

## Ordering rules

1. Group stickies into chronological process steps
2. For each step, emit in this order: `readmodel` (if any), `command`, `event`
3. List all `actor` items first (one per distinct role involved)
4. List `policy` items after the timeline stickies
5. List `system` items after policies
6. List `hotspot` items last, with `x` and `y` coordinates placing them near the relevant timeline step

## Example output

```json
[
  {"type": "actor", "text": "Customer"},
  {"type": "actor", "text": "Warehouse Team"},

  {"type": "readmodel", "text": "Product catalogue"},
  {"type": "command", "text": "Place order"},
  {"type": "event", "text": "Order placed"},
  {"type": "command", "text": "Process payment"},
  {"type": "event", "text": "Payment confirmed"},

  {"type": "policy", "text": "If payment fails - cancel order"},

  {"type": "system", "text": "Stripe"},
  {"type": "system", "text": "Warehouse WMS"},

  {"type": "hotspot", "text": "Payment timeout issues", "x": 500, "y": 300}
]
```

## My process document

<PASTE YOUR DOCUMENT HERE>
