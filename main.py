import requests
import hashlib
import winsound
import webbrowser

from time import sleep
from datetime import datetime

def get_website_hash(url):
    response = requests.get(url)
    response.raise_for_status()
    return hashlib.sha256(response.content).hexdigest()

def notify_with_sound():
    winsound.Beep(frequency=523, duration=500)
    winsound.Beep(frequency=523, duration=500)
    winsound.Beep(frequency=784, duration=500)
    winsound.Beep(frequency=784, duration=500)
    winsound.Beep(frequency=880, duration=500)
    winsound.Beep(frequency=880, duration=500)
    winsound.Beep(frequency=784, duration=1000)

def log_update(filename, timestamp, initial_hash, new_hash):
    with open(filename, 'a') as log_file:
        log_entry = f"[{timestamp}]: WEBSITE UPDATED! (initial hash: {initial_hash}, new hash: {new_hash})\n"
        log_file.write(log_entry)

if __name__ == '__main__':
    url = 'https://shop.travisscott.com/'
    # url = 'https://us.supreme.com/collections/all'
    monitor_delay = 3

    initial_hash = get_website_hash(url)
    dropped = False

    while not dropped:
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_hash = get_website_hash(url)
            # print("Current hash: " + current_hash)
            # print("Initial hash: " + initial_hash)
            if current_hash != initial_hash:
                print(f"[{current_time}]: WEBSITE UPDATED!")
                webbrowser.open(url)
                notify_with_sound()
                log_update('log.txt', current_time, initial_hash, current_hash) 
                initial_hash = current_hash
                # dropped = True
            else:
                print(f"[{current_time}]: IDLE")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching website: {e}")

        sleep(monitor_delay)