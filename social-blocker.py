#run script with: sudo python3 social-blocker.py
import os
import sys
from datetime import datetime

#variables
HOST_PATH = "/etc/hosts" #back up this file by doing: cp /etc/hosts host-backup.txt (if file needs to be reverted to original state do: cp host-backup.txt /etc/hosts)
REDIRECT_IP = "127.0.0.1"
BLOCK_COMMENT = "## Blocked Sites"
BLOCKED_SITES = [
    "www.youtube.com", "youtube.com",
    "www.instagram.com", "instagram.com",
    "www.facebook.com", "facebook.com",
    "www.tiktok.com", "tiktok.com"
]
JOURNAL_FILE = "social-unblock-journal.txt"

#functions

def block_sites():
    with open(HOST_PATH, "r+") as file:
        content = file.read()
        file.seek(0,os.SEEK_END)
        if BLOCK_COMMENT not in content:
            file.write(f"{BLOCK_COMMENT}\n")
        for site in BLOCKED_SITES:
            entry = f"{REDIRECT_IP} {site}\n"
            if entry not in content:
                file.write(entry)
    
    print("Socials blocked")

def unblock_sites():
    log_entry = input("Why do you want to block socials? (100 char minimum): ")
    if len(log_entry) < 100:
        print(f"\nExplaination too short: ({len(log_entry)}). Unblock request denied")
        sys.exit(0)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(JOURNAL_FILE, 'a') as file:
        file.write(f"[{timestamp}] {log_entry}\n\n")
    
    with open(HOST_PATH, 'r') as file:
        lines = file.readlines()

    new_lines = []

    for line in lines:
        if line.strip() == BLOCK_COMMENT:
            continue
        if line.startswith(REDIRECT_IP) and any (site in line for site in BLOCKED_SITES):
            continue
        new_lines.append(line)
    
    with open(HOST_PATH, 'w') as file:
        file.writelines(new_lines)

    print("Socials unblocked")

def main():
    print("1. Block social media \n2.Unblock social media")
    choice = input("Choose an option (1 or 2): ")
    if choice == "1":
        block_sites()
    elif choice == "2":
        unblock_sites()
    else:
        print("Invalid choice")
        sys.exit(0)

if __name__ == "__main__":
    main()
    
