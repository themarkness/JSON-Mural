import os
import sys
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

load_dotenv()

client_id = os.environ["MURAL_CLIENT_ID"]
client_secret = os.environ["MURAL_CLIENT_SECRET"]
mural_id = os.environ["MURAL_ID"]

redirect_uri = "http://127.0.0.1:8000/"
authorization_base_url = "https://app.mural.co/api/public/v1/authorization/oauth2/"
token_url = "https://app.mural.co/api/public/v1/authorization/oauth2/token"
scopes = ["murals:read murals:write"]


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.server.auth_response = self.requestline[4:-9]


def get_session():
    httpd = HTTPServer(("127.0.0.1", 8000), ServerHandler)
    mural = OAuth2Session(client_id, scope=scopes, redirect_uri=redirect_uri)
    authorization_url, state = mural.authorization_url(authorization_base_url)
    webbrowser.open(authorization_url)
    httpd.handle_request()
    redirect_response = "https://127.0.0.1:8000" + httpd.auth_response
    mural.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)
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
}


def post_sticky(session, text, x=0, y=0, colour=None):
    url = f"https://app.mural.co/api/public/v1/murals/{mural_id}/widgets/sticky-note"
    body = {"x": x, "y": y, "text": text, "shape": "rectangle"}
    if colour:
        body["style"] = {"backgroundColor": COLOURS.get(colour, colour)}
    resp = session.post(url, json=body)
    resp.raise_for_status()
    return resp.json()


def post_stickies(session, stickies):
    for s in stickies:
        result = post_sticky(session, s["text"], s.get("x", 0), s.get("y", 0), s.get("colour"))
        print(f"Created: {s['text']}")
    return len(stickies)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", default=None)
    parser.add_argument("--x", type=int, default=0)
    parser.add_argument("--y", type=int, default=0)
    parser.add_argument("--colour", choices=list(COLOURS.keys()), default=None)
    parser.add_argument("--file", help="JSON file with array of stickies")
    args = parser.parse_args()

    session = get_session()

    if args.file:
        with open(args.file) as f:
            stickies = json.load(f)
        count = post_stickies(session, stickies)
        print(f"Posted {count} stickies")
    else:
        result = post_sticky(session, args.text, args.x, args.y, args.colour)
        print(f"Created sticky: {result['id']}")
