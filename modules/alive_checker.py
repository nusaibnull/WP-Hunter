import requests

def is_site_alive(url, timeout=5):
    try:
        res = requests.get(url, timeout=timeout)
        return res.status_code < 400
    except:
        return False
