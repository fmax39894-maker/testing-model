import os
import json
import random
import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
TIMEOUT = 12
MAX_IMAGE_BYTES = 8 * 1024 * 1024

# Add your public image/page URLs here. Keep each URL in quotes.
IMAGE_LINKS = [
    "https://example.com/photo.jpg",
    "https://example.com/gallery-page",
    "https://share.google/YiHPovirrbRRBcy6H",
]

def get_json(url, **kwargs):
    response = requests.get(url, timeout=TIMEOUT, **kwargs)
    response.raise_for_status()
    return response

def image_from_page(url):
    """Return a public image URL found on a direct image URL or HTML page."""
    try:
        r = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0"},
            stream=True,
            allow_redirects=True,
        )
        content_type = r.headers.get("Content-Type", "").lower()

        if r.ok and content_type.startswith("image/"):
            final_url = r.url
            r.close()
            return final_url

        r.close()

        page = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True,
        )
        if not page.ok:
            return None

        soup = BeautifulSoup(page.text, "html.parser")

        # Prefer social preview images.
        for key in ("og:image", "twitter:image", "twitter:image:src"):
            tag = soup.find("meta", attrs={"property": key}) or soup.find(
                "meta", attrs={"name": key}
            )
            if tag and tag.get("content"):
                candidate = urljoin(page.url, tag["content"].strip())
                if is_image(candidate):
                    return candidate

        # Otherwise inspect a few normal image tags.
        for tag in soup.find_all("img")[:30]:
            candidate = (
                tag.get("src")
                or tag.get("data-src")
                or tag.get("data-original")
            )
            if candidate:
                candidate = urljoin(page.url, candidate.strip())
                if is_image(candidate):
                    return candidate

    except requests.RequestException:
        log.info("Could not inspect URL: %s", url)
    return None

def is_image(url):
    try:
        r = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0"},
            stream=True,
            allow_redirects=True,
        )
        ctype = r.headers.get("Content-Type", "").lower()
        length = r.headers.get("Content-Length")
        okay = r.ok and ctype.startswith("image/")
        if length and int(length) > MAX_IMAGE_BYTES:
            okay = False
        r.close()
        return okay
    except (requests.RequestException, ValueError):
        return False

def read_links():
    return [
        link.strip()
        for link in IMAGE_LINKS
        if link.strip() and not link.strip().startswith("#")
    ]

def telegram(method, payload):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    r = requests.post(url, json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")
    return data.get("result")

def send_text(chat_id, text, reply_to=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    telegram("sendMessage", payload)

def handle_update(update):
    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    text = (message.get("text") or "").strip()
    if not text:
        return

    # Accept /image and /image@YourBotName in groups.
    command = text.split()[0].split("@")[0].lower()
    if command != "/image":
        return

    chat_id = message.get("chat", {}).get("id")
    reply_to = message.get("message_id")
    if not chat_id:
        return

    try:
        links = read_links()
        random.shuffle(links)

        for link in links:
            image_url = image_from_page(link)
            if image_url:
                # Telegram fetches the public image URL and sends one photo.
                telegram("sendPhoto", {
                    "chat_id": chat_id,
                    "photo": image_url,
                    "reply_to_message_id": reply_to,
                })
                return

        send_text(chat_id, "No working image was found in the GitHub list.", reply_to)

    except Exception:
        log.exception("Image command failed")
        send_text(chat_id, "Sorry, I couldn't fetch an image right now. Please try again.", reply_to)

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Telegram image bot webhook is running."
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        # No webhook secret is required in this simplified setup.
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            update = json.loads(raw.decode("utf-8"))
            if isinstance(update, dict):
                handle_update(update)
        except Exception:
            log.exception("Webhook request failed")

        # Acknowledge Telegram so it does not repeatedly retry this update.
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ok")
