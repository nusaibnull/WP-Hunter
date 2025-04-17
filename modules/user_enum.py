import requests
import re

def enumerate_usernames(site, max_ids=10):
    usernames = []
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
    }

    for i in range(1, max_ids + 1):
        try:
            url = f"{site}/?author={i}"
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)

            if response.status_code == 200:
                # Check for redirection to /author/username/
                match = re.search(r"/author/([a-zA-Z0-9_\-]+)/", response.url)
                if match:
                    username = match.group(1)
                    if username not in usernames:
                        usernames.append(username)
                        print(f"[+] Found username: {username}")
        except requests.RequestException:
            continue

    return usernames
