# 🛠️ WordPress Plugin Exploit Scanner

A modular and flexible WordPress plugin vulnerability scanner that checks for outdated or vulnerable plugins, performs exploit attempts, brute-force attacks (optional), and generates reports. Intended for **ethical hacking**, **penetration testing**, and **bug bounty research** purposes only.

---

## ⚠️ Disclaimer

> **This tool is for authorized security testing only. Do not use it on systems you do not have permission to test. Unauthorized use is illegal.**

---

## 🚀 Features

- ✅ Scan WordPress sites for vulnerable plugins
- 🔍 Choose between Fast Scan, Deep Scan, or Custom Plugin list
- 💀 Attempt known shell upload exploits (e.g., `wp-file-manager`)
- 🔓 Optional brute-force login attack (with default creds)
- 📝 Generates a report for each scanned site
- 🧱 Modular design (easy to extend with your own plugins/exploits)

---

## 📂 Project Structure

---

## 📦 Installation

1. **Clone the repo**
   ```bash
   git clone [https://github.com/nusaibnull/wp-exploit-scanner.git](https://github.com/nusaibnull/WP-Hunter.git
   cd wp-exploit-scanner
pip3 install -r requirements.txt

🔸 Scan a single target directly
python main.py --target https://example.com

🧨 Enable exploit attempt
python main.py --exploit

🔑 Enable brute force login
python main.py --brute

🔥 Do everything (exploit + brute force)
python main.py --all

🧠 Plugin Scan Modes
When prompted:

Fast Scan → Scan only top plugins

Deep Scan → Scan all known plugins

Custom List → Load from custom plugin list

🛡️ Ethical Use Only
Built for researchers, CTFs, bug bounty, and red teamers under legal authorization. Respect the rules.
