import os
import re

ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")


def extract_mural_id(input_str):
    """Extract mural ID from a URL or return as-is if already an ID."""
    # Match mural ID pattern in URL: workspace.timestamp
    match = re.search(r"/m/[^/]+/(\w+\.\d+)", input_str)
    if match:
        return match.group(1)
    # Already in ID format
    if re.match(r"^\w+\.\d+$", input_str.strip()):
        return input_str.strip()
    return None


def run_setup():
    print("=== Mural Sticky Poster Setup ===\n")

    # Load existing values as defaults
    existing = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    existing[k] = v

    # Client ID
    default = existing.get("MURAL_CLIENT_ID", "")
    prompt = f"Client ID [{default}]: " if default else "Client ID: "
    client_id = input(prompt).strip() or default
    if not client_id:
        print("Client ID is required. Get it from https://developers.mural.co → Your apps")
        return

    # Client Secret
    default = existing.get("MURAL_CLIENT_SECRET", "")
    prompt = f"Client Secret [{default}]: " if default else "Client Secret: "
    client_secret = input(prompt).strip() or default
    if not client_secret:
        print("Client Secret is required.")
        return

    # Mural ID — accept URL or raw ID
    default = existing.get("MURAL_ID", "")
    prompt = f"Mural board URL or ID [{default}]: " if default else "Mural board URL or ID: "
    raw = input(prompt).strip() or default
    mural_id = extract_mural_id(raw)
    if not mural_id:
        print(f"Could not extract mural ID from: {raw}")
        print("Expected a URL like https://app.mural.co/t/workspace/m/workspace/workspace.1234567890/...")
        print("Or an ID like: workspace.1234567890")
        return

    # Write .env
    with open(ENV_FILE, "w") as f:
        f.write(f"MURAL_CLIENT_ID={client_id}\n")
        f.write(f"MURAL_CLIENT_SECRET={client_secret}\n")
        f.write(f"MURAL_ID={mural_id}\n")

    print(f"\n✓ Config saved to .env")
    print(f"  Mural ID: {mural_id}")
    print(f"\nRun `python main.py` to get started.")


if __name__ == "__main__":
    run_setup()
