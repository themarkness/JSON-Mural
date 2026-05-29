import json
import sys
from post_sticky import get_session, post_sticky, COLOURS

# Swim lane y-positions (top to bottom)
# readmodel, command, event share the SAME row (the main timeline)
# actor, policy, system have their own rows
LANES = {
    "actor": 0,
    "readmodel": 200,
    "command": 200,
    "event": 200,
    "policy": 400,
    "system": 600,
}

STICKY_WIDTH = 200
GAP = 50


def layout_event_storm(steps):
    """Convert event storm steps into positioned stickies.

    readmodel, command, event share a single row — they flow left-to-right
    together as the main timeline.
    actor, policy, system flow independently in their own rows.
    hotspot uses explicit x, y to sit near its related sticky.
    """
    # Single counter for the main timeline (readmodel/command/event)
    timeline_counter = 0
    lane_counters = {"actor": 0, "policy": 0, "system": 0}
    stickies = []

    for step in steps:
        stype = step["type"]

        if stype == "hotspot":
            stickies.append({
                "text": step["text"],
                "x": step["x"],
                "y": step["y"],
                "colour": stype,
            })
            continue

        if stype in ("readmodel", "command", "event"):
            if "column" in step:
                col = step["column"]
                timeline_counter = max(timeline_counter, col + 1)
            else:
                col = timeline_counter
                timeline_counter += 1
        else:
            if "column" in step:
                col = step["column"]
                lane_counters[stype] = max(lane_counters[stype], col + 1)
            else:
                col = lane_counters[stype]
                lane_counters[stype] += 1

        x = col * (STICKY_WIDTH + GAP)
        y = LANES[stype]
        stickies.append({
            "text": step["text"],
            "x": x,
            "y": y,
            "colour": stype,
        })

    return stickies


if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else "event_storm.json"
    with open(file) as f:
        steps = json.load(f)

    stickies = layout_event_storm(steps)
    session = get_session()

    for s in stickies:
        post_sticky(session, s["text"], s["x"], s["y"], s["colour"])
        print(f"Posted: [{s['colour']}] {s['text']}")

    print(f"\nDone — {len(stickies)} stickies posted")
