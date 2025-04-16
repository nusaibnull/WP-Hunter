import requests

# Enumerate plugins from target website
def enumerate_plugins(target, plugin_list):
    found_plugins = []
    print(f"\n[*] Scanning plugins on: {target}")
    for plugin in plugin_list:
        url = f"{target}/wp-content/plugins/{plugin}/"
        try:
            res = requests.get(url, timeout=8)
            if res.status_code == 200 and "Index of" in res.text:
                print(f"[+] Found plugin: {plugin}")
                found_plugins.append(plugin)
                
                # Handle new plugin detection
                handle_new_plugin(plugin)
                notify_user_about_new_plugin(plugin)
                
        except:
            continue
    return found_plugins

def handle_new_plugin(plugin, db_path="data/exploits_db.json"):
    # Load the existing database
    db = load_exploits_from_db(db_path)
    
    if plugin not in db:
        print(f"[-] New plugin detected: {plugin}")
        # Add new plugin to the exploit database (could be marked as unknown)
        db[plugin] = {"exploit": "Unknown"}
        
        # Save the updated database
        with open(db_path, "w") as f:
            json.dump(db, f, indent=4)
        
        print(f"[+] New plugin added to the exploit database: {plugin}")
    else:
        print(f"[+] Plugin {plugin} already exists in the exploit database.")

def notify_user_about_new_plugin(plugin):
    print(f"\n[!] New plugin detected: {plugin}")
    print(f"[!] No exploits found for {plugin}. Please verify the plugin for vulnerabilities.")

def load_exploits_from_db(db_path="data/exploits_db.json"):
    with open(db_path, "r") as f:
        db = json.load(f)
    return db
