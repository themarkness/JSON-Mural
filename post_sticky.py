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


def post_sticky(session, text, x=0, y=0):
    url = f"https://app.mural.co/api/public/v1/murals/{mural_id}/widgets/sticky-note"
    body = {"x": x, "y": y, "text": text, "shape": "rectangle"}
    resp = session.post(url, json=body)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--x", type=int, default=0)
    parser.add_argument("--y", type=int, default=0)
    args = parser.parse_args()

    session = get_session()
    result = post_sticky(session, args.text, args.x, args.y)
    print(f"Created sticky: {json.dumps(result, indent=2)}")
