import json
import os
import sys
from post_sticky import get_session, post_sticky, COLOURS

LEGEND_FILE = os.path.join(os.path.dirname(__file__), "legend.json")

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


LEGEND_X = -300


def post_legend(session):
    with open(LEGEND_FILE) as f:
        items = json.load(f)
    for i, item in enumerate(items):
        y = i * (STICKY_WIDTH + GAP)
        colour = item["type"] if item["type"] != "hotspot" else "hotspot"
        post_sticky(session, item["text"], LEGEND_X, y, colour)
    print(f"Posted legend ({len(items)} items)")


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
    session = get_session()

    print("Populating the board with the event storm legend...")
    post_legend(session)

    answer = input("\nDo you want to populate the board with the example event storm? (y/n): ").strip().lower()
    if answer == "y":
        with open("example_event_storm.json") as f:
            steps = json.load(f)
        stickies = layout_event_storm(steps)
        for s in stickies:
            post_sticky(session, s["text"], s["x"], s["y"], s["colour"])
            print(f"Posted: [{s['colour']}] {s['text']}")
        print(f"\nDone — {len(stickies)} stickies posted")
    else:
        print("\nCustom event storm input coming soon. For now, edit example_event_storm.json and re-run.")
