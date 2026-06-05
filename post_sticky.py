import os
import sys
import json
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from dotenv import load_dotenv

ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")


def load_config():
    load_dotenv(ENV_FILE)
    missing = [k for k in ("MURAL_CLIENT_ID", "MURAL_CLIENT_SECRET", "MURAL_ID") if not os.environ.get(k)]
    if missing:
        print("Config not found. Running setup...\n")
        from setup import run_setup
        run_setup()
        load_dotenv(ENV_FILE, override=True)
        missing = [k for k in ("MURAL_CLIENT_ID", "MURAL_CLIENT_SECRET", "MURAL_ID") if not os.environ.get(k)]
        if missing:
            sys.exit("Setup incomplete. Please run `python setup.py` to configure.")
    return os.environ["MURAL_CLIENT_ID"], os.environ["MURAL_CLIENT_SECRET"], os.environ["MURAL_ID"]


client_id, client_secret, mural_id = load_config()

redirect_uri = "http://127.0.0.1:8000/"
authorization_base_url = "https://app.mural.co/api/public/v1/authorization/oauth2/"
token_url = "https://app.mural.co/api/public/v1/authorization/oauth2/token"
refresh_url = "https://app.mural.co/api/public/v1/authorization/oauth2/refresh"
scopes = ["murals:read murals:write"]

TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".token.json")
RATE_LIMIT_DELAY = 0.5  # seconds between API calls


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.server.auth_response = self.requestline[4:-9]


def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token, f)


def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return None


def get_session():
    token = load_token()
    if token:
        mural = OAuth2Session(client_id, token=token, scope=scopes, redirect_uri=redirect_uri)
        try:
            resp = mural.get("https://app.mural.co/api/public/v1/users/me")
            if resp.ok:
                return mural
        except TokenExpiredError:
            pass

    # Fresh auth flow
    httpd = HTTPServer(("127.0.0.1", 8000), ServerHandler)
    mural = OAuth2Session(client_id, scope=scopes, redirect_uri=redirect_uri)
    authorization_url, state = mural.authorization_url(authorization_base_url)
    webbrowser.open(authorization_url)
    httpd.handle_request()
    redirect_response = "https://127.0.0.1:8000" + httpd.auth_response
    token = mural.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)
    save_token(token)
    return mural


# Event storming colour map (8-char hex with alpha)
COLOURS = {
    "event": "#FF6B35FF",       # Orange
    "command": "#4A90D9FF",     # Blue
    "actor": "#F5D547FF",       # Yellow
    "readmodel": "#7BC67EFF",   # Green
    "policy": "#9B59B6FF",      # Purple
    "system": "#FF69B4FF",      # Pink
    "hotspot": "#FF0000FF",     # Red
    "aggregate": "#F0E68CFF",   # Khaki
}


def post_sticky(session, text, x=0, y=0, colour=None):
    url = f"https://app.mural.co/api/public/v1/murals/{mural_id}/widgets/sticky-note"
    body = {"x": x, "y": y, "text": text, "shape": "rectangle"}
    if colour:
        hex_colour = COLOURS.get(colour) or (colour if colour.startswith("#") else None)
        if hex_colour:
            body["style"] = {"backgroundColor": hex_colour}
    resp = session.post(url, json=body)
    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 5))
        print(f"Rate limited. Waiting {retry_after}s...")
        time.sleep(retry_after)
        resp = session.post(url, json=body)
    resp.raise_for_status()
    time.sleep(RATE_LIMIT_DELAY)
    return resp.json()


def post_stickies(session, stickies):
    for s in stickies:
        result = post_sticky(session, s["text"], s.get("x", 0), s.get("y", 0), s.get("colour"))
        print(f"Created: {s['text']}")
    return len(stickies)



