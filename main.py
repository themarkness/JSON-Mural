import os
import sys
import json
from post_sticky import get_session, post_sticky, post_stickies, COLOURS
from event_storm import layout_event_storm, post_legend

EXAMPLE_FILE = os.path.join(os.path.dirname(__file__), "example_event_storm.json")


def do_single_sticky(session):
    text = input("Sticky text: ").strip()
    if not text:
        print("No text provided.")
        return
    x = int(input("x position [0]: ").strip() or "0")
    y = int(input("y position [0]: ").strip() or "0")
    print(f"\nColours: {', '.join(COLOURS.keys())}")
    colour = input("Colour [event]: ").strip() or "event"
    result = post_sticky(session, text, x, y, colour)
    print(f"\n✓ Posted sticky: {result['id']}")


def do_event_storm(session):
    filepath = input(f"Path to event storm JSON (Enter for example): ").strip()
    if not filepath:
        filepath = EXAMPLE_FILE
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath) as f:
        steps = json.load(f)

    print("\nPosting legend...")
    post_legend(session)

    stickies = layout_event_storm(steps)
    print(f"Posting {len(stickies)} stickies...\n")
    for s in stickies:
        post_sticky(session, s["text"], s["x"], s["y"], s["colour"])
        print(f"  [{s['colour']}] {s['text']}")
    print(f"\n✓ Done — {len(stickies)} stickies posted")


def do_batch_stickies(session):
    filepath = input("Path to stickies JSON: ").strip()
    if not filepath or not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath) as f:
        stickies = json.load(f)
    count = post_stickies(session, stickies)
    print(f"\n✓ Posted {count} stickies")


def main():
    print("=== Mural CLI ===\n")

    session = get_session()
    print("✓ Authenticated\n")

    print("What would you like to do?\n")
    print("  1. Post an event storm")
    print("  2. Post a single sticky")
    print("  3. Post batch stickies from JSON")
    print("  4. Re-run setup")

    choice = input("\nChoice [1]: ").strip() or "1"

    if choice == "1":
        do_event_storm(session)
    elif choice == "2":
        do_single_sticky(session)
    elif choice == "3":
        do_batch_stickies(session)
    elif choice == "4":
        from setup import run_setup
        run_setup()
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
