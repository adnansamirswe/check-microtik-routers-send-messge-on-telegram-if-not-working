import time
import logging
import requests
from socks5_opcopy import auth
from requests.exceptions import RequestException

# Configuration
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
CHAT_ID = 'your_chat_id'
CHECK_INTERVAL = 5 * 60  # 5 minutes in seconds
ROUTER_FILE_PATH = 'ip:user:password.txt'
ROUTER_PORT = 8725  # Port used for authentication

# Set up logging
logging.basicConfig(level=logging.INFO)

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logging.info(f"Message sent: {message}")
    except RequestException as e:
        logging.error(f"Failed to send message: {e}")

def check_router(ip, user, password):
    try:
        api = auth(ip, user, password, ROUTER_PORT)
        logging.info(f"Authenticated with router {ip}")
        return True
    except Exception as e:
        logging.error(f"Failed to authenticate with router {ip}: {e}")
        return False

def main():
    while True:
        logging.info("Checking routers...")
        with open(ROUTER_FILE_PATH, 'r') as file:
            routers = file.read().splitlines()

        for line in routers:
            parts = line.strip().split(':')
            if len(parts) != 3:
                logging.warning(f"Invalid line format: {line}")
                continue

            ip, user, password = parts
            if not check_router(ip, user, password):
                message = f'Router {ip} is not working.'
                logging.info(message)  # Log to console for debugging
                send_telegram_message(message)

        logging.info(f"Waiting for {CHECK_INTERVAL / 60} minutes before next check.")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
