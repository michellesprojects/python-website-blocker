import os
import sys
import time
import threading
from datetime import datetime

HOST_PATH = "/etc/hosts"
REDIRECT = "127.0.0.1"
BLOCK_COMMENT = "## Blocked Sites"
BLOCKED_SITES = [
"www.youtube.com", "youtube.com",
"www.instagram.com", "instagram.com",
"www.substack.com", "substack.com",
"www.x.com", "x.com",
"www.facebook.com", "facebook.com",
"www.reddit.com", "reddit.com"
]
JOURNAL_FILE = "unblock-request-journal.txt"

def add_block_entries():
    with open(HOST_PATH, 'r+') as file:
        content = file.read()
        file.seek(0,os.SEEK_END)
        if BLOCK_COMMENT not in content:
            file.write(f"{BLOCK_COMMENT}\n")
        for site in BLOCKED_SITES:
            entry_ipv4 = f"{REDIRECT} {site}\n"
            entry_ipv6 = f"::1 {site}\n"
            if entry_ipv4 not in content:
                file.write(entry_ipv4)
            if entry_ipv6 not in content:
                file.write(entry_ipv6)

def block_sites():
    add_block_entries()
    print("Blocked socials.")

def remove_block_entries():
    with open(HOST_PATH, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines:
        if line.strip() == "## Blocked Sites":
            continue
        if (line.startswith(REDIRECT) or line.startswith("::1")) and any(site in line for site in BLOCKED_SITES):
            continue
        new_lines.append(line)
    with open(HOST_PATH, 'w') as file:
        file.writelines(new_lines)

def unblock_sites():
    log_entry = input("Why do you want to unblock socials? (100 char explaination minimum)").strip()
    if len(log_entry) < 100:
        print(f"\nExplaination too short ({len(log_entry)}).Unblock Request denied")
        sys.exit(0)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(JOURNAL_FILE, 'a') as log:
        log.write(f"[{timestamp}] {log_entry}\n\n")
    remove_block_entries()
    print("Unblocked YouTube, Instagram, and Facebook.")

def unblock_sites_timed():
    log_entry = input("Why do you want to unblock socials for 20 minutes? (100 char explaination minimum)").strip()
    if len(log_entry) < 100:
        print(f"\nExplaination too short ({len(log_entry)}).Unblock Request denied")
        sys.exit(0)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(JOURNAL_FILE, 'a') as log:
        log.write(f"[{timestamp}] 20-minute unblock: {log_entry}\n\n")
    remove_block_entries()
    print("Unblocked socials for 20 minutes. Timer started.")
    timer_thread = threading.Thread(target=reblock_after_timeout, daemon=False)
    timer_thread.start()

def close_browsers():
    system = sys.platform
    if system == "darwin":
        os.system("pkill -f 'Google Chrome'")
        os.system("pkill -f 'Firefox'")
        os.system("pkill -f 'Safari'")
    elif system == "linux":
        os.system("pkill -f chrome")
        os.system("pkill -f firefox")
    elif system == "win32":
        os.system("taskkill /F /IM chrome.exe")
        os.system("taskkill /F /IM firefox.exe")
        os.system("taskkill /F /IM msedge.exe")

def reblock_after_timeout():
    duration = 20 * 60
    elapsed = 0
    while elapsed < duration:
        remaining_minutes = (duration - elapsed) // 60
        print(f"{remaining_minutes} minute warning")
        time.sleep(60)
        elapsed += 60
    add_block_entries()
    close_browsers()
    print("Sites re-blocked and browsers closed.")

def main():
    print("1. Block social media\n2. Unblock social media\n3. Unblock sites for 20 minutes")
    choice = input("Choose an option (1, 2, or 3): ")
    if choice == "1":
        block_sites()
    elif choice == "2":
        unblock_sites()
    elif choice == "3":
        unblock_sites_timed()
    else:
        print("Invalid choice.")
        sys.exit(0)

if __name__ == "__main__":
    main()
