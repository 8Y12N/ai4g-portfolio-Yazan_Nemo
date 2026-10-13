import csv, json, os, re, time
from datetime import datetime, timezone
import websocket

SERVICES = [
    # cloud / hosting
    "aws", "amazon web services", "azure", "google cloud", "gcp", "cloudflare",
    "akamai", "fastly", "digitalocean", "heroku", "vercel", "netlify", "oracle cloud",
    # platforms / work tools
    "github", "gitlab", "slack", "discord", "microsoft 365", "office 365", "outlook",
    "teams", "gmail", "google drive", "zoom", "whatsapp", "chatgpt", "openai",
    # Dutch internet / telecom
    "kpn", "ziggo", "odido", "t-mobile", "vodafone", "delta fiber", "caiway",
    # Dutch digital public services / banking
    "digid", "mijnoverheid", "ing", "rabobank", "abn amro", "bunq", "ideal",
]

OUTAGE = [
    # English
    "outage", "outages", "is down", "are down", "went down", "goes down", "down again",
    "down for everyone", "down for anyone", "down right now", "is it down",
    "not working", "isn't working", "stopped working", "not loading", "won't load",
    "can't connect", "cannot connect", "can't log in", "cannot log in", "can't login",
    "service disruption", "degraded performance", "server error", "servers are down",
    "bad gateway", "gateway timeout", "502", "503", "no internet", "no signal",
    # Dutch
    "storing", "storingen", "landelijke storing", "verstoring", "ligt eruit",
    "ligt er uit", "ligt plat", "werkt niet", "doet het niet", "doet niks",
    "kan niet inloggen", "geen verbinding", "geen internet", "geen bereik",
    "onbereikbaar", "hapert", "haperingen", "valt steeds weg", "valt weg",
]

# \b = whole words only, so "down" won't match "download"
svc_re = re.compile(r"\b(" + "|".join(map(re.escape, SERVICES)) + r")\b")
out_re = re.compile(r"\b(" + "|".join(map(re.escape, OUTAGE)) + r")\b")

DATA, CURSOR = "data/posts.csv", "data/cursor.txt"
URL = "wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post"
MAX_SECONDS = 8 * 60 

os.makedirs("data", exist_ok=True)
now_us = int(time.time() * 1_000_000)
try:
    cursor = int(open(CURSOR).read())
except (FileNotFoundError, ValueError):
    cursor = now_us - 15 * 60 * 1_000_000

ws = websocket.create_connection(f"{URL}&cursor={cursor}", timeout=30)
new_file = not os.path.exists(DATA)
start, scanned, hits, last = time.time(), 0, 0, cursor

with open(DATA, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new_file:
        w.writerow(["time_utc", "service", "lang", "text"])
    while time.time() - start < MAX_SECONDS:
        e = json.loads(ws.recv())
        last = e.get("time_us", last)
        if last >= now_us:
            break 
        c = e.get("commit", {})
        if c.get("operation") != "create":
            continue
        rec = c.get("record", {})
        text = rec.get("text", "")
        scanned += 1
        low = text.lower()
        s = svc_re.search(low)
        if s and out_re.search(low):
            hits += 1
            ts = datetime.fromtimestamp(last / 1e6, timezone.utc).isoformat(timespec="seconds")
            w.writerow([ts, s.group(1), ",".join(rec.get("langs", [])), text.replace("\n", " ")])

ws.close()
open(CURSOR, "w").write(str(last + 1))
print(f"scanned {scanned} posts, saved {hits} outage posts")