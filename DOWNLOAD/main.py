import random
import string
import requests
import time
from pystyle import Write, Colors
import os

base_url = "https://discordapp.com/api/v6/entitlements/gift-codes/"

# Discord webhook URL (initialize as empty)
webhook_url = ""

# Open valid file in append mode for saving valid codes
valid_file = open("ValidGift.txt", "a", encoding="utf-8")
valid_file.close()  # Close the file temporarily after opening it

def send_to_discord(message):
    """Function to send messages to the Discord webhook."""
    if webhook_url:  # Check if webhook URL is set
        payload = {"content": message}
        try:
            requests.post(webhook_url, json=payload)
        except requests.exceptions.RequestException as e:
            Write.Print(f"[Error] Failed to send webhook: {e}\n", Colors.red_to_yellow, interval=0.000)
    else:
        Write.Print("[Error] Webhook URL is not set.\n", Colors.red_to_yellow, interval=0.000)

while True:
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen

    Write.Print("""
████████╗███████╗███╗░░██╗███████╗░█████╗░██╗░██████╗  ███╗░░██╗██╗████████╗██████╗░░█████╗░
╚══██╔══╝██╔════╝████╗░██║╚════██║██╔══██╗╚█║██╔════╝  ████╗░██║██║╚══██╔══╝██╔══██╗██╔══██╗
░░░██║░░░█████╗░░██╔██╗██║░░███╔═╝██║░░██║░╚╝╚█████╗░  ██╔██╗██║██║░░░██║░░░██████╔╝██║░░██║
░░░██║░░░██╔══╝░░██║╚████║██╔══╝░░██║░░██║░░░░╚═══██╗  ██║╚████║██║░░░██║░░░██╔══██╗██║░░██║
░░░██║░░░███████╗██║░╚███║███████╗╚█████╔╝░░░██████╔╝  ██║░╚███║██║░░░██║░░░██║░░██║╚█████╔╝
░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚══════╝░╚════╝░░░░╚═════╝░  ╚═╝░░╚══╝╚═╝░░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░

░██████╗░███████╗███╗░░██╗
██╔════╝░██╔════╝████╗░██║
██║░░██╗░█████╗░░██╔██╗██║
██║░░╚██╗██╔══╝░░██║╚████║
╚██████╔╝███████╗██║░╚███║
░╚═════╝░╚══════╝╚═╝░░╚══╝
                                 
                    """, Colors.blue_to_purple, interval=0)

    Write.Print("""
---------------------
| (1) NitroGen      |
| (2) Set Webhook   |
| (3) Exit          |
---------------------
""", Colors.red_to_purple, interval=0.001)

    choice = Write.Input("\n>>:", Colors.blue_to_red, interval=0)

    if choice == "3":
        exit()  # Exit the program
    elif choice == "2":
        # Get the webhook URL from the user
        webhook_url = Write.Input("Enter your Discord Webhook URL: ", Colors.blue_to_red, interval=0)
        Write.Print(f"Webhook URL set to: {webhook_url}\n", Colors.green_to_yellow, interval=0)
    elif choice == "1":
        # Open files in append mode to avoid overwriting existing data
        valid_file = open("ValidGift.txt", "a", encoding="utf-8")

        while True:
            # Generate a random 16-character alphanumeric code
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            gift_url = f"discord.gift/{code}"

            try:
                r = requests.get(f"{base_url}{code}?with_application=false&with_subscription_plan=true", timeout=5)

                # If the request is successful and returns a valid gift code (status code 200)
                if r.status_code == 200:
                    Write.Print(f"[Valid] {gift_url}\n", Colors.green_to_yellow, interval=0.000)
                    valid_file.write(f"{gift_url}\n")  # Write valid code to file
                    valid_file.flush()  # Flush the file to ensure it is written immediately

                    # Send the valid gift code to the Discord webhook
                    send_to_discord(f"Valid Discord Gift Code: {gift_url}")

                else:
                    Write.Print(f"[Invalid] {gift_url}\n", Colors.red_to_yellow, interval=0.000)

            except requests.exceptions.RequestException as e:
                # Handle request errors gracefully
                Write.Print(f"[Error] {gift_url}\n", Colors.red_to_yellow, interval=0.000)

        # Close files when done (although this will never happen due to the infinite loop)
        valid_file.close()
