# 🛠️ WordPress Plugin Exploit Scanner

A modular and flexible **WordPress vulnerability scanner** that detects vulnerable plugins, attempts known exploits (like shell uploads), performs **brute-force attacks** (optional), and generates detailed reports.

> 🧠 Designed for **ethical hackers**, **penetration testers**, and **bug bounty hunters**.

---

## ⚠️ Disclaimer

> **This tool is intended for authorized security testing only.**
>
> 🛑 Do **NOT** use on systems you don’t own or have permission to test.  
> Unauthorized access is **illegal** and punishable by law.

---

## 🚀 Features

- 🔍 Scan for vulnerable WordPress plugins
- ⚡ Fast Scan / Deep Scan / Custom Plugin List modes
- 💀 Shell exploit attempts (e.g., `wp-file-manager`)
- 🔓 Optional brute-force login using common passwords
- 📄 Generates JSON/console-based reports
- 🧱 Modular code structure (easy to add new modules/exploits)
- 🎯 Single target or bulk scanning via `sites_list.txt`

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nusaibnull/WP-Hunter.git
   cd WP-Hunter
   pip install -r requirements.txt
## Run Cloud Shell

<p align="left">
  <a href="https://shell.cloud.google.com/cloudshell/open?cloudshell_git_repo=https://github.com/nusaibnull/WP-Hunter.git&tutorial=README.md" target="_blank"><img src="https://gstatic.com/cloudssh/images/open-btn.svg"></a>
</p>
# 🔥 Help
python main.py --help

# 🔥 Run Target Site
python main.py --target https://example.com

# 🔥 Run exploits
python main.py --exploit

# 🔥 Run  brute-force
python main.py --brute

# 🔥 Run both exploits + brute-force + verbose + threads
python main.py --all --threads 10 --verbose

🔥 Run both exploits + brute-force
python main.py --all

🧨 Bulk Brute Force Tool (Optional)

python brute_force_all.py --threads 10 --verbose --save-json

🛡️ Ethical Use Only

This tool is for:

✅ Penetration Testers (with permission)

✅ Bug Bounty Programs

✅ Ethical Hackers

✅ Cybersecurity Researchers

Respect the rules, get legal authorization before testing!

👨‍💻 Author
Made with ❤️ by @nullbrainBD
For any help or collaboration, feel free to connect!

